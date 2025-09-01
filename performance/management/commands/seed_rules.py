from django.core.management.base import BaseCommand
from performance.models import ScoreRule

DEFAULT_RULES = [
    # key, label, points (>0 = penalty, <0 = credit), active
    ("late_1",              "Late (10:16–10:30)",                     +1.0, True),
    ("late_2",              "Late (10:31–10:45)",                     +2.0, True),
    ("late_3",              "Late (>10:45)",                          +3.0, True),
    ("missing_eod",         "Missing EOD report",                     +3.0, True),
    ("generic_eod",         "Generic/insufficient EOD",               +1.0, True),
    ("irrelevant_activity", "Irrelevant activity during work",        +5.0, True),
    ("uninformed_absence",  "Uninformed early leave/absence",         +5.0, True),
    ("visitor_breach",      "Visitor breach",                         +2.0, True),

    ("weekly_on_time",      "On time all week",                       -5.0, True),
    ("weekly_eod_ok",       "EOD correct all week",                   -5.0, True),
    ("weekly_no_irrelevant","No irrelevant activity all week",        -3.0, True),
    ("good_work_bonus",     "Good work bonus",                        -2.0, True),

    ("manual_adjust",       "Manual adjust",                           0.0, True),
]

class Command(BaseCommand):
    help = "Create or update default ScoreRule entries with our canonical points."

    def handle(self, *args, **options):
        created, updated = 0, 0
        for key, label, points, active in DEFAULT_RULES:
            obj, was_created = ScoreRule.objects.update_or_create(
                key=key, defaults={"label": label, "points": points, "active": active}
            )
            created += int(was_created)
            updated += int(not was_created)
        self.stdout.write(self.style.SUCCESS(
            f"Seeded rules. Created: {created}, Updated: {updated}"
        ))
