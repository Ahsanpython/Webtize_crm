from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    title = models.CharField(max_length=80, blank=True)
    department = models.CharField(max_length=80, blank=True)
    include_in_performance = models.BooleanField(default=True)  # <-- ensure this line exists

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ScoreRule(models.Model):
    """
    Admin-editable points per 'unit' (can be negative).
    Examples (matching your policy):
      - late_1 (-1), late_2 (-2), late_3 (-3)
      - uninformed_absence (-5)
      - missing_eod (-3), generic_eod (-1)
      - irrelevant_activity (-5), visitor_breach (-2)
      - weekly_on_time (+5), weekly_eod_ok (+5), weekly_no_irrelevant (+3)
      - good_work_bonus (+1..+20), manual_adjust (+/-)
    """
    key = models.SlugField(unique=True)
    label = models.CharField(max_length=120)
    points = models.FloatField(default=0)   # points per 'quantity'
    unit = models.CharField(max_length=20, default="unit")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.points}/{self.unit})"

class ScoreEvent(models.Model):
    """A concrete adjustment for a user in a day (auto or manual)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="score_events")
    rule = models.ForeignKey(ScoreRule, on_delete=models.PROTECT)
    quantity = models.FloatField(default=1.0)
    points_delta = models.FloatField()             # stored for audit
    date = models.DateField(default=timezone.now)  # when it happened
    notes = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="score_records")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.points_delta is None or kwargs.pop("recalc", False):
            self.points_delta = (self.rule.points or 0) * (self.quantity or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} {self.points_delta:+} on {self.date} ({self.rule.key})"

class ScoreSnapshot(models.Model):
    """Monthly cached totals for fast dashboards (optional, we also compute ad-hoc)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="score_snapshots")
    period_start = models.DateField()
    period_end = models.DateField()
    total_points = models.FloatField(default=0)

    class Meta:
        unique_together = ("user", "period_start", "period_end")

    def __str__(self):
        return f"{self.user} {self.total_points} [{self.period_start}..{self.period_end}]"