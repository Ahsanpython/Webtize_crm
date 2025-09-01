
from django.urls import path
from .api_views import SummaryView, RevenueByMonthView, InvoiceStatusView, ProjectBurnView
urlpatterns = [
    path("summary/", SummaryView.as_view()),
    path("revenue_by_month/", RevenueByMonthView.as_view()),
    path("invoice_status/", InvoiceStatusView.as_view()),
    path("project_burn/", ProjectBurnView.as_view()),
]
