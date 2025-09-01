# D:\pycrm\performance\services.py
from __future__ import annotations
from datetime import date
from calendar import monthrange

from django.db.models import Sum
from django.utils.timezone import now

from .models import ScoreEvent, ScoreRule

BASE_SCORE = 100.0


def month_bounds(dt: date | None = None) -> tuple[date, date]:
    """Return first/last day of the given (or current) month."""
    if dt is None:
        dt = now().date()
    start = date(dt.year, dt.month, 1)
    end = date(dt.year, dt.month, monthrange(dt.year, dt.month)[1])
    return start, end


def team_current_month(users_qs):
    """
    Convention used in your admin:

      - Credits are POSITIVE (e.g. +5 weekly_on_time).
      - Penalties are NEGATIVE (e.g. -1 late_1).

    Score = 100 + sum(credits) - abs(sum(penalties))

    We read directly from ScoreEvent.points_delta.
    """
    start, end = month_bounds()
    rows = []

    for u in users_qs:
        ev = ScoreEvent.objects.filter(user=u, date__gte=start, date__lte=end)

        # credits (+)
        credits = ev.filter(points_delta__gt=0).aggregate(s=Sum("points_delta"))["s"] or 0

        # penalties (negative -> take magnitude for display)
        penalties = abs(ev.filter(points_delta__lt=0).aggregate(s=Sum("points_delta"))["s"] or 0)

        score = BASE_SCORE + float(credits) - float(penalties)

        rows.append({
            "id": u.id,
            "name": (u.get_full_name() or u.username),
            "adds": float(credits),        # for green bars / chip
            "deds": float(penalties),      # for red bars / chip (magnitude)
            "score": float(score),
        })

    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows


def ensure_default_rules() -> None:
    """
    Safe helper used by EnsureRulesAPI: creates/updates your default rule set.
    You can run it via POST /performance/api/seed_rules/ or call from shell.
    """
    defaults = [
        # key,                 label,                                 points
        ("late_1",            "Late (10:16–10:30)",                   -1),
        ("late_2",            "Late (10:31–10:45)",                   -2),
        ("late_3",            "Late (>10:45)",                        -3),
        ("uninformed_absence","Uninformed early leave/absence",       -5),
        ("missing_eod",       "Missing EOD report",                   -3),
        ("generic_eod",       "Generic/insufficient EOD",             -1),
        ("irrelevant_activity","Irrelevant activity",                 -5),
        ("visitor_breach",    "Visitor breach",                       -2),

        ("weekly_on_time",    "On time all week",                      5),
        ("weekly_eod_ok",     "EOD correct all week",                  5),
        ("weekly_no_irrelevant","No irrelevant activity all week",     3),
        ("good_work_bonus",   "Good work bonus",                       2),

        ("manual_adjust",     "Manual adjust",                         0),
    ]
    for key, label, pts in defaults:
        ScoreRule.objects.update_or_create(
            key=key,
            defaults={"label": label, "points": pts, "unit": "unit", "active": True},
        )
