
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Invoice

class InvoiceListView(ListView):
    model = Invoice
    template_name = "invoices/list.html"
    context_object_name = "invoices"

class InvoiceCreateView(CreateView):
    model = Invoice
    fields = ["client","project","number","issue_date","due_date","status","subtotal","tax","total","paid_amount"]
    success_url = reverse_lazy("invoice_list")
    template_name = "invoices/form.html"



# --- CSV export for monthly revenue (paid invoices) -------------------
from datetime import date
from calendar import monthrange
from django.views import View
from django.http import HttpResponse
from django.db.models import Sum
import csv

from .models import Invoice

class ExportRevenueCSV(View):
    """
    GET /invoices/export/revenue_csv/?month=YYYY-MM   (month optional; defaults to current month)
    Exports only invoices with status = 'paid'
    """
    def get(self, request):
        q = request.GET.get("month")
        if q:
            y, m = map(int, q.split("-"))
            start = date(y, m, 1)
        else:
            t = date.today()
            start = date(t.year, t.month, 1)

        end = date(start.year, start.month, monthrange(start.year, start.month)[1])

        qs = (
            Invoice.objects
            .filter(status="paid", issue_date__gte=start, issue_date__lte=end)
            .select_related("client")
            .order_by("issue_date", "id")
        )

        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = f'attachment; filename="revenue_{start:%Y_%m}.csv"'
        w = csv.writer(resp)
        w.writerow(["Date", "Invoice #", "Client", "Status", "Paid Amount"])

        for inv in qs:
            inv_no = getattr(inv, "number", None) or inv.id
            client_name = getattr(getattr(inv, "client", None), "name", "") or ""
            w.writerow([
                f"{inv.issue_date:%Y-%m-%d}",
                inv_no,
                client_name,
                inv.status,
                f"{float(inv.paid_amount or 0):.2f}",
            ])

        total = qs.aggregate(s=Sum("paid_amount"))["s"] or 0
        w.writerow([])
        w.writerow(["TOTAL", "", "", "", f"{float(total):.2f}"])
        return resp
