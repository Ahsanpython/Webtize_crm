
from django.urls import path
from . import views
urlpatterns = [
    path("", views.TimesheetListView.as_view(), name="timesheet_list"),
    path("create/", views.TimesheetCreateView.as_view(), name="timesheet_create"),
]
