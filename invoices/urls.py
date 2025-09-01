
from django.urls import path
from . import views
urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),
    path("create/", views.InvoiceCreateView.as_view(), name="invoice_create"),
]
