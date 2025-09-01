from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from performance.models import EmployeeProfile
from performance.services import ensure_default_rules

TEAM = [
    ("ahsan",   "Ahsan"),
    ("haseeb",  "Haseeb"),
    ("yazdan",  "Yazdan"),
    ("mohsin",  "Mohsin"),
    ("hassam",  "Hassam"),
    ("malangi", "Malangi"),
    ("jut",     "Jut"),
]

DEFAULT_PASSWORD = "Webtize@123"   # <-- change after first login

class Command(BaseCommand):
    help = "Creates the 7 team users, their profiles (included in performance), and seeds default rules."

    def handle(self, *args, **options):
        User = get_user_model()
        created_users = []

        with transaction.atomic():
            for username, first in TEAM:
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": first,
                        "email": f"{username}@example.com",
                        "is_active": True,
                    },
                )
                if created:
                    user.set_password(DEFAULT_PASSWORD)
                    user.save()
                    created_users.append(username)

                # Ensure a profile and inclusion on dashboard
                prof, _ = EmployeeProfile.objects.get_or_create(user=user)
                if not prof.include_in_performance:
                    prof.include_in_performance = True
                    prof.save()

        ensure_default_rules()

        self.stdout.write(self.style.SUCCESS(
            "Bootstrap complete.\n"
            f"Users created: {created_users or 'none (already existed)'}\n"
            f"Default password for new users: {DEFAULT_PASSWORD} (please change).\n"
            "Score rules ensured."
        ))
