from django import forms
from .models import Expense

class DateInput(forms.DateInput):
    input_type = "date"

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "category", "amount", "payment_method", "description", "vendor"]
        labels = { "vendor": "Payee" }
        widgets = {
            "date": DateInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "0.00"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Internet bill for August"}),
            "vendor": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., PTCL / Stationery shop / Cash"}),
        }
