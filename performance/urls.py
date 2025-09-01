from django.urls import path
from .views import (
    PerformanceDashboardView,
    TeamSummaryAPI,
    MonthlyTrendAPI,
    EnsureRulesAPI,
    ExportCSVView,
    ExportPDFView,
)

urlpatterns = [
    path("", PerformanceDashboardView.as_view(), name="perf_dashboard"),

    # APIs
    path("api/team/", TeamSummaryAPI.as_view()),
    path("api/monthly_trend/", MonthlyTrendAPI.as_view()),
    path("api/seed_rules/", EnsureRulesAPI.as_view()),

    # Exports
    path("export/csv/", ExportCSVView.as_view(), name="perf_export_csv"),
    path("export/pdf/", ExportPDFView.as_view(), name="perf_export_pdf"),
]
