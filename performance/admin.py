from django.contrib import admin
from .models import EmployeeProfile, ScoreRule, ScoreEvent, ScoreSnapshot

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "department")
    search_fields = ("user__username", "user__first_name", "user__last_name", "department")

@admin.register(ScoreRule)
class ScoreRuleAdmin(admin.ModelAdmin):
    list_display = ("key", "label", "points", "unit", "active")
    list_filter = ("active",)
    search_fields = ("key", "label")

@admin.register(ScoreEvent)
class ScoreEventAdmin(admin.ModelAdmin):
    exclude = ("quantity", "points_delta")  # no quantity in quick award
    list_display = ("date", "user", "rule", "points_delta", "notes")
    list_filter = ("rule", "date")
    search_fields = ("user__username", "user__first_name", "user__last_name", "notes")
    autocomplete_fields = ("user", "rule")

    def save_model(self, request, obj, form, change):
        obj.quantity = 1
        obj.points_delta = obj.rule.points
        if not obj.recorded_by_id:
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)



@admin.register(ScoreSnapshot)
class ScoreSnapshotAdmin(admin.ModelAdmin):
    list_display = ("user", "period_start", "period_end", "total_points")
    list_filter = ("period_start",)
