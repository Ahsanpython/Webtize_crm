
# from django.urls import path
# from . import views
# urlpatterns = [
#     path("", views.DashboardView.as_view(), name="dashboard"),
# ]


from django.urls import path
from . import views
from .api_views import (
    SummaryView,
    RevenueByMonthView,
    InvoiceStatusView,
    ProjectBurnView,
    ExpensesByCategoryView,
    RevenueVsExpensesView,
)

urlpatterns = [
    # Page (HTML dashboard)
    path("", views.DashboardView.as_view(), name="dashboard"),

    # JSON APIs used by the dashboard JS
    path("api/summary/", SummaryView.as_view(), name="api_summary"),
    path("api/revenue_by_month/", RevenueByMonthView.as_view(), name="api_revenue_by_month"),
    path("api/invoice_status/", InvoiceStatusView.as_view(), name="api_invoice_status"),
    path("api/project_burn/", ProjectBurnView.as_view(), name="api_project_burn"),
    path("api/expenses_by_category/", ExpensesByCategoryView.as_view(), name="api_expenses_by_category"),
    path("api/revenue_vs_expenses/", RevenueVsExpensesView.as_view(), name="api_revenue_vs_expenses"),
]
