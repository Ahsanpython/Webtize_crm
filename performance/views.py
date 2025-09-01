# D:\pycrm\performance\views.py
from datetime import date
from calendar import monthrange
from io import BytesIO
import csv

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EmployeeProfile, ScoreEvent
from .services import team_current_month, ensure_default_rules

User = get_user_model()


# ----------------------------
# Dashboard (HTML)
# ----------------------------
class PerformanceDashboardView(TemplateView):
    template_name = "performance/dashboard.html"


# ----------------------------
# APIs used by the dashboard
# ----------------------------
class TeamSummaryAPI(APIView):
    """
    Current-month per-person metrics, returned in the same meaning
    that the services layer uses:

      - rows[i]["adds"] = credits (sum of positive points_delta)
      - rows[i]["deds"] = penalties magnitude (abs of negative points_delta)
      - rows[i]["score"] = 100 + credits - penalties

      We pass these through to the charts and also provide 'net' (= credits - penalties).
    """
    def get(self, request):
        user_ids = (
            EmployeeProfile.objects
            .filter(include_in_performance=True, user__is_active=True)
            .values_list("user_id", flat=True)
        )
        qs = User.objects.filter(id__in=user_ids)

        rows = team_current_month(qs)  # [{name, adds(credits +), deds(penalties +), score}, ...]

        labels     = [r["name"] for r in rows]
        credits    = [float(r["adds"]) for r in rows]          # +ve
        penalties  = [float(r["deds"]) for r in rows]          # +ve magnitude
        scores     = [float(r["score"]) for r in rows]         # 100 + c - p
        net        = [c - p for c, p in zip(credits, penalties)]

        return Response({
            "labels": labels,
            "scores": scores,
            "credits": credits,
            "penalties": penalties,
            "net": net,
        })


class MonthlyTrendAPI(APIView):
    """
    Team totals for last 6 months + current.
    Uses ScoreEvent.points_delta (NOT a 'points' field).
    """
    def get(self, request):
        today = date.today()

        # Build month list: 6 months back + current (7 total)
        months = []
        for i in range(6, -1, -1):  # 6..0
            y = today.year
            m = today.month - i
            while m <= 0:
                m += 12
                y -= 1
            months.append((y, m))

        labels, team_scores, credits_list, penalties_list = [], [], [], []

        inc_user_ids = (
            EmployeeProfile.objects
            .filter(include_in_performance=True, user__is_active=True)
            .values_list("user_id", flat=True)
        )

        for (yy, mm) in months:
            start = date(yy, mm, 1)
            end = date(yy, mm, monthrange(yy, mm)[1])

            qs = ScoreEvent.objects.filter(
                user_id__in=inc_user_ids,
                date__gte=start, date__lte=end
            )

            # IMPORTANT: use points_delta
            c_sum = qs.filter(points_delta__gt=0).aggregate(s=Sum("points_delta"))["s"] or 0
            p_sum = abs(qs.filter(points_delta__lt=0).aggregate(s=Sum("points_delta"))["s"] or 0)

            labels.append(f"{start:%b %Y}")
            credits_list.append(float(c_sum))
            penalties_list.append(float(p_sum))
            team_scores.append(float(100 + c_sum - p_sum))

        return Response({
            "labels": labels,
            "team_scores": team_scores,
            "credits": credits_list,
            "penalties": penalties_list,
        })


class EnsureRulesAPI(APIView):
    """POST to ensure default rules exist/are updated."""
    def post(self, request):
        ensure_default_rules()
        return Response({"ok": True})


# ----------------------------
# Exports
# ----------------------------
class ExportCSVView(View):
    """
    /performance/export/csv/?month=YYYY-MM  (defaults to current month)
    """
    def get(self, request):
        q = request.GET.get("month")
        if q:
            y, m = map(int, q.split("-"))
            start = date(y, m, 1)
        else:
            t = date.today()
            start = date(t.year, t.month, 1)
        end = date(start.year, start.month, monthrange(start.year, start.month)[1])

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="performance_{start:%Y_%m}.csv"'
        writer = csv.writer(response)
        writer.writerow(["Date", "User", "Rule", "Points Δ"])

        events = (
            ScoreEvent.objects
            .select_related("user", "rule")
            .filter(date__gte=start, date__lte=end)
            .order_by("date", "user__username")
        )
        for e in events:
            full = getattr(e.user, "get_full_name", lambda: e.user.username)() or e.user.username
            writer.writerow([f"{e.date:%Y-%m-%d}", full, getattr(e.rule, "label", ""), e.points_delta])
        return response


class ExportPDFView(View):
    """
    /performance/export/pdf/?month=YYYY-MM  (defaults to current month)
    Requires: reportlab
    """
    def get(self, request):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm
        except Exception:
            return HttpResponse("ReportLab is required. pip install reportlab",
                                content_type="text/plain", status=500)

        q = request.GET.get("month")
        if q:
            y, m = map(int, q.split("-"))
            start = date(y, m, 1)
        else:
            t = date.today()
            start = date(t.year, t.month, 1)
        end = date(start.year, start.month, monthrange(start.year, start.month)[1])

        inc_user_ids = (
            EmployeeProfile.objects
            .filter(include_in_performance=True, user__is_active=True)
            .values_list("user_id", flat=True)
        )

        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        W, H = A4

        c.setFont("Helvetica-Bold", 14)
        c.drawString(2*cm, H-2*cm, f"Performance Summary — {start:%B %Y}")
        y_cursor = H - 3*cm
        c.setFont("Helvetica", 10)

        users = User.objects.filter(id__in=inc_user_ids).order_by("first_name", "username")
        for u in users:
            ev = ScoreEvent.objects.filter(user=u, date__gte=start, date__lte=end)
            # IMPORTANT: use points_delta
            credits   = ev.filter(points_delta__gt=0).aggregate(s=Sum("points_delta"))["s"] or 0
            penalties = abs(ev.filter(points_delta__lt=0).aggregate(s=Sum("points_delta"))["s"] or 0)
            score     = 100 + credits - penalties

            display = getattr(u, "get_full_name", lambda: u.username)() or u.username
            line = f"{display:25}  Credits:{credits:5.1f}  Penalties:{penalties:5.1f}  Score:{score:5.1f}"
            c.drawString(2*cm, y_cursor, line)
            y_cursor -= 0.7*cm
            if y_cursor < 2*cm:
                c.showPage()
                y_cursor = H - 2*cm
                c.setFont("Helvetica", 10)

        c.showPage()
        c.save()
        pdf = buf.getvalue()
        buf.close()

        resp = HttpResponse(content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="performance_{start:%Y_%m}.pdf"'
        resp.write(pdf)
        return resp
