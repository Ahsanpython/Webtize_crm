
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
