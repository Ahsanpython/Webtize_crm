
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("clients/", include("clients.urls")),
    path("projects/", include("projects.urls")),
    path('expenses/', include('expenses.urls')),
    path("timesheets/", include("timesheets.urls")),
    path("invoices/", include("invoices.urls")),
    path("api/", include("dashboard.api_urls")),
    path("performance/", include("performance.urls")),
]
