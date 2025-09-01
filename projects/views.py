
# from django.views.generic import ListView, CreateView, DetailView
# from django.urls import reverse_lazy
# from .models import Project

# class ProjectListView(ListView):
#     model = Project
#     template_name = "projects/list.html"
#     context_object_name = "projects"

# class ProjectCreateView(CreateView):
#     model = Project
#     fields = ["client","name","description","budget_amount","budget_currency","estimated_hours","start_date","end_date","status"]
#     success_url = reverse_lazy("project_list")
#     template_name = "projects/form.html"

# class ProjectDetailView(DetailView):
#     model = Project
#     template_name = "projects/detail.html"


from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Sum, F
from datetime import date
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"

class ProjectCreateView(CreateView):
    model = Project
    fields = ["client","name","description","budget_amount","budget_currency","estimated_hours","start_date","end_date","status"]
    success_url = reverse_lazy("project_list")
    template_name = "projects/form.html"

class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.object

        # Hours
        spent_hours = p.timesheets.aggregate(s=Sum("hours"))["s"] or 0
        hours_left = float((p.estimated_hours or 0) - (spent_hours or 0))
        progress_pct = 0.0
        if p.estimated_hours and float(p.estimated_hours) > 0:
            progress_pct = max(0.0, min(100.0, float(spent_hours) / float(p.estimated_hours) * 100.0))

        # Money (billable hours * hourly_rate)
        spent_cost = p.timesheets.filter(billable=True).aggregate(
            s=Sum(F("hours") * F("hourly_rate"))
        )["s"] or 0
        budget_left = float((p.budget_amount or 0) - (spent_cost or 0))

        # Invoices / payments
        invoiced = p.invoices.aggregate(s=Sum("total"))["s"] or 0
        paid = p.invoices.aggregate(s=Sum("paid_amount"))["s"] or 0
        outstanding = float((invoiced or 0) - (paid or 0))

        # Time left (days)
        days_left = None
        if p.end_date:
            days_left = (p.end_date - date.today()).days

        ctx.update({
            "spent_hours": float(spent_hours),
            "hours_left": hours_left,
            "progress_pct": round(progress_pct, 1),

            "budget": float(p.budget_amount or 0),
            "spent_cost": float(spent_cost or 0),
            "budget_left": budget_left,

            "invoiced": float(invoiced or 0),
            "paid": float(paid or 0),
            "outstanding": float(outstanding or 0),

            "days_left": days_left,
        })
        return ctx
