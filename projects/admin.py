
from django.contrib import admin
from .models import Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name","client","budget_amount","estimated_hours","status","start_date","end_date")
    list_filter = ("status","start_date")
    search_fields = ("name","client__name")
