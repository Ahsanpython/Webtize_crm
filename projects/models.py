
from django.db import models
from django.utils import timezone
from clients.models import Client

class Project(models.Model):
    STATUS_CHOICES = [
        ("pending","Pending"),
        ("active","Active"),
        ("completed","Completed"),
        ("on_hold","On Hold"),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    budget_currency = models.CharField(max_length=8, default="PKR")
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.client.name})"
