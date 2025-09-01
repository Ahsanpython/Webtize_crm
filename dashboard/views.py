from datetime import date, timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view
from rest_framework.response import Response

from invoices.models import Invoice
from expenses.models import Expense

from django.views.generic import TemplateView
class DashboardView(TemplateView):
    template_name = "dashboard.html"
