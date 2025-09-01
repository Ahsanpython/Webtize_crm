
from django.contrib import admin
from .models import TimesheetEntry
@admin.register(TimesheetEntry)
class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ("user","project","date","hours","billable","hourly_rate")
    list_filter = ("billable","date","project")
    search_fields = ("user__username","project__name")
