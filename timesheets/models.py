
from django.db import models
from django.conf import settings
from projects.models import Project

class TimesheetEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="timesheets")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="timesheets")
    date = models.DateField()
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    billable = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]

    def cost(self):
        return (self.hourly_rate or 0) * float(self.hours)

    def __str__(self):
        return f"{self.user} - {self.project} - {self.date} ({self.hours}h)"
