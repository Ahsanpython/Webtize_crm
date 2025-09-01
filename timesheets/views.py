
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TimesheetEntry

class TimesheetListView(LoginRequiredMixin, ListView):
    model = TimesheetEntry
    template_name = "timesheets/list.html"
    context_object_name = "entries"

    def get_queryset(self):
        return TimesheetEntry.objects.select_related("project","user")[:200]

class TimesheetCreateView(LoginRequiredMixin, CreateView):
    model = TimesheetEntry
    fields = ["project","date","hours","billable","hourly_rate","notes"]
    success_url = reverse_lazy("timesheet_list")
    template_name = "timesheets/form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
