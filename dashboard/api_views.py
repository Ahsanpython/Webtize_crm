
# from datetime import date, timedelta
# from django.db.models import Sum, Count, F
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from invoices.models import Invoice
# from projects.models import Project
# from timesheets.models import TimesheetEntry

# class SummaryView(APIView):
#     def get(self, request):
#         today = date.today()
#         start_30 = today - timedelta(days=30)
#         revenue_30d = Invoice.objects.filter(status="paid", issue_date__gte=start_30).aggregate(
#             s=Sum("paid_amount")
#         )["s"] or 0
#         outstanding = sum([inv.outstanding() for inv in Invoice.objects.exclude(status="paid")])
#         active_projects = Project.objects.filter(status__in=["active","pending"]).count()
#         hours_30d = TimesheetEntry.objects.filter(date__gte=start_30).aggregate(s=Sum("hours"))["s"] or 0
#         return Response({
#             "revenue_30d": float(revenue_30d),
#             "outstanding": float(outstanding),
#             "active_projects": active_projects,
#             "hours_30d": float(hours_30d),
#         })

# class RevenueByMonthView(APIView):
#     def get(self, request):
#         # naive 6-month sum by issue month
#         from django.db.models.functions import TruncMonth
#         qs = Invoice.objects.filter(status="paid").annotate(m=TruncMonth("issue_date")).values("m").annotate(
#             total=Sum("paid_amount")
#         ).order_by("m")
#         labels = [x["m"].strftime("%b %Y") for x in qs if x["m"]]
#         data = [float(x["total"] or 0) for x in qs]
#         return Response({"labels": labels, "data": data})

# class InvoiceStatusView(APIView):
#     def get(self, request):
#         qs = Invoice.objects.values("status").annotate(c=Count("id"))
#         labels = [x["status"].capitalize() for x in qs]
#         data = [x["c"] for x in qs]
#         return Response({"labels": labels, "data": data})

# class ProjectBurnView(APIView):
#     def get(self, request):
#         # compare project budgets vs cost from timesheets (billable hours * hourly_rate)
#         labels, budget, spent = [], [], []
#         for p in Project.objects.all()[:20]:
#             labels.append(p.name[:20])
#             budget.append(float(p.budget_amount or 0))
#             cost = TimesheetEntry.objects.filter(project=p, billable=True).aggregate(
#                 s=Sum(F("hours") * F("hourly_rate"))
#             )["s"] or 0
#             spent.append(float(cost))
#         return Response({"labels": labels, "budget": budget, "spent": spent})



# dashboard/api_views.py

from datetime import date, timedelta
from collections import OrderedDict

from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response

from invoices.models import Invoice
from projects.models import Project
from timesheets.models import TimesheetEntry
from expenses.models import Expense   # <-- NEW


class SummaryView(APIView):
    """
    OLD keys are preserved:
      - revenue_30d, outstanding, active_projects, hours_30d
    NEW keys added:
      - expenses_30d, net_30d  (revenue_30d - expenses_30d)
    """
    def get(self, request):
        today = date.today()
        start_30 = today - timedelta(days=30)

        # revenue in last 30d (paid invoices)
        revenue_30d = Invoice.objects.filter(
            status="paid", issue_date__gte=start_30
        ).aggregate(s=Sum("paid_amount"))["s"] or 0

        # outstanding using your model's outstanding() helper
        outstanding = sum(
            [inv.outstanding() for inv in Invoice.objects.exclude(status="paid")]
        )

        # active projects, hours 30d (same as before)
        active_projects = Project.objects.filter(status__in=["active", "pending"]).count()
        hours_30d = TimesheetEntry.objects.filter(date__gte=start_30).aggregate(
            s=Sum("hours")
        )["s"] or 0

        # NEW: company expenses last 30d and net
        expenses_30d = Expense.objects.filter(date__gte=start_30).aggregate(
            s=Sum("amount")
        )["s"] or 0
        net_30d = (revenue_30d or 0) - (expenses_30d or 0)

        return Response({
            "revenue_30d": float(revenue_30d),
            "outstanding": float(outstanding),
            "active_projects": active_projects,
            "hours_30d": float(hours_30d),
            # NEW
            "expenses_30d": float(expenses_30d),
            "net_30d": float(net_30d),
        })


class RevenueByMonthView(APIView):
    # unchanged
    def get(self, request):
        # naive 6-month sum by issue month
        from django.db.models.functions import TruncMonth  # keep your local import
        qs = Invoice.objects.filter(status="paid").annotate(m=TruncMonth("issue_date")).values("m").annotate(
            total=Sum("paid_amount")
        ).order_by("m")
        labels = [x["m"].strftime("%b %Y") for x in qs if x["m"]]
        data = [float(x["total"] or 0) for x in qs]
        return Response({"labels": labels, "data": data})


class InvoiceStatusView(APIView):
    # unchanged
    def get(self, request):
        qs = Invoice.objects.values("status").annotate(c=Count("id"))
        labels = [x["status"].capitalize() for x in qs]
        data = [x["c"] for x in qs]
        return Response({"labels": labels, "data": data})


class ProjectBurnView(APIView):
    # unchanged
    def get(self, request):
        # compare project budgets vs cost from timesheets (billable hours * hourly_rate)
        labels, budget, spent = [], [], []
        for p in Project.objects.all()[:20]:
            labels.append(p.name[:20])
            budget.append(float(p.budget_amount or 0))
            cost = TimesheetEntry.objects.filter(project=p, billable=True).aggregate(
                s=Sum(F("hours") * F("hourly_rate"))
            )["s"] or 0
            spent.append(float(cost))
        return Response({"labels": labels, "budget": budget, "spent": spent})


# ------------- NEW ENDPOINTS ------------- #

class ExpensesByCategoryView(APIView):
    """
    This month’s expenses grouped by category.
    Returns: { labels: [...], data: [...] }
    """
    def get(self, request):
        today = date.today()
        qs = Expense.objects.filter(date__year=today.year, date__month=today.month)
        data = qs.values("category").annotate(s=Sum("amount")).order_by()
        label_map = dict(Expense.Category.choices)  # code -> human label
        labels = [label_map.get(row["category"], row["category"]) for row in data]
        values = [float(row["s"] or 0) for row in data]
        return Response({"labels": labels, "data": values})


class RevenueVsExpensesView(APIView):
    """
    Monthly revenue (paid invoices) vs expenses.
    Returns: { labels: ['Jan 2025', ...], revenue: [...], expenses: [...] }
    """
    def get(self, request):
        rev = (
            Invoice.objects.filter(status="paid")
            .annotate(m=TruncMonth("issue_date"))
            .values("m").annotate(s=Sum("paid_amount")).order_by("m")
        )
        exp = (
            Expense.objects
            .annotate(m=TruncMonth("date"))
            .values("m").annotate(s=Sum("amount")).order_by("m")
        )

        months = OrderedDict()
        for r in rev:
            months[r["m"]] = {"rev": float(r["s"] or 0), "exp": 0.0}
        for e in exp:
            months.setdefault(e["m"], {"rev": 0.0, "exp": 0.0})
            months[e["m"]]["exp"] = float(e["s"] or 0)

        labels = [m.strftime("%b %Y") for m in months.keys()]
        revenues = [v["rev"] for v in months.values()]
        expenses = [v["exp"] for v in months.values()]
        return Response({"labels": labels, "revenue": revenues, "expenses": expenses})
