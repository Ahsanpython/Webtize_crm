
from django.db import models
from clients.models import Client
from projects.models import Project

class Invoice(models.Model):
    STATUS_CHOICES = [
        ("draft","Draft"),
        ("sent","Sent"),
        ("paid","Paid"),
        ("overdue","Overdue"),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="invoices")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices")
    number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.id:
            self.subtotal = sum([i.amount() for i in self.items.all()]) if hasattr(self, "items") else self.subtotal
            self.total = (self.subtotal or 0) + (self.tax or 0)
        super().save(*args, **kwargs)

    def outstanding(self):
        return (self.total or 0) - (self.paid_amount or 0)

    def __str__(self):
        return f"{self.number} - {self.client.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def amount(self):
        return (self.quantity or 0) * (self.unit_price or 0)

    def __str__(self):
        return f"{self.description} ({self.invoice.number})"
