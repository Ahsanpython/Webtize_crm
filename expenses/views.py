from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from datetime import date
from .models import Expense
from .forms import ExpenseForm


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/list.html"
    context_object_name = "expenses"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # month filter ?month=YYYY-MM
        m = self.request.GET.get('month')
        qs = self.get_queryset()
        if m:
            y, mm = m.split('-')
            qs = qs.filter(date__year=int(y), date__month=int(mm))
        ctx['total_month'] = qs.aggregate(s=Sum('amount'))['s'] or 0
        ctx['selected_month'] = m
        return ctx

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy('expense_list')

class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/form.html"
    success_url = reverse_lazy('expense_list')



class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expenses/confirm_delete.html"
    success_url = reverse_lazy('expense_list')


# ======================================================================



# --- CSV export for monthly expenses ---------------------------------
from datetime import date
from calendar import monthrange
from django.views import View
from django.http import HttpResponse
from django.db.models import Sum
import csv

from .models import Expense

class ExportExpensesCSV(View):
    """
    GET /expenses/export/csv/?month=YYYY-MM   (month is optional; defaults to current month)
    """
    def get(self, request):
        q = request.GET.get("month")  # 'YYYY-MM'
        if q:
            y, m = map(int, q.split("-"))
            start = date(y, m, 1)
        else:
            t = date.today()
            start = date(t.year, t.month, 1)

        end = date(start.year, start.month, monthrange(start.year, start.month)[1])

        qs = (
            Expense.objects
            .filter(date__gte=start, date__lte=end)
            .select_related("project")
            .order_by("date", "id")
        )

        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = f'attachment; filename="expenses_{start:%Y_%m}.csv"'
        w = csv.writer(resp)
        w.writerow(["Date", "Category", "Description", "Vendor", "Payment method", "Amount", "Project"])

        for e in qs:
            w.writerow([
                f"{e.date:%Y-%m-%d}",
                getattr(e, "category", "") or "",
                e.description or "",
                getattr(e, "vendor", "") or "",
                getattr(e, "payment_method", "") or "",
                f"{float(e.amount or 0):.2f}",
                getattr(getattr(e, "project", None), "name", "") or "",
            ])

        total = qs.aggregate(s=Sum("amount"))["s"] or 0
        w.writerow([])
        w.writerow(["TOTAL", "", "", "", "", f"{float(total):.2f}", ""])
        return resp
