from django.db import models
from datetime import date

class Expense(models.Model):
    class Category(models.TextChoices):
        RENT = 'rent', 'Rent'
        INTERNET = 'internet', 'Internet'
        UTILITIES = 'utilities', 'Utilities (Electric/Water/Gas)'
        SUPPLIES = 'supplies', 'Office Supplies'
        SALARY = 'salary', 'Salaries'
        MARKETING = 'marketing', 'Marketing'
        TRAVEL = 'travel', 'Travel'
        TAXES = 'taxes', 'Taxes/Govt Fees'
        MAINTENANCE = 'maintenance', 'Maintenance/Repairs'
        OTHER = 'other', 'Other'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        BANK = 'bank', 'Bank Transfer'
        CARD = 'card', 'Card'
        MOBILE = 'mobile', 'Mobile Wallet'

    date = models.DateField(default=date.today)
    category = models.CharField(max_length=32, choices=Category.choices)
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    vendor = models.CharField(max_length=120, blank=True)
    payment_method = models.CharField(max_length=16, choices=PaymentMethod.choices, default=PaymentMethod.BANK)
    # optional linking (if some expense is specific to a client/project)
    client = models.ForeignKey('clients.Client', null=True, blank=True, on_delete=models.SET_NULL, related_name='expenses')
    project = models.ForeignKey('projects.Project', null=True, blank=True, on_delete=models.SET_NULL, related_name='expenses')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.amount} on {self.date}"
