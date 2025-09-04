
from django.urls import path
from . import views
from .views import ExportRevenueCSV 
urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),
    path("create/", views.InvoiceCreateView.as_view(), name="invoice_create"),
    path("export/revenue_csv/", ExportRevenueCSV.as_view(), name="revenue_export_csv"),
]
