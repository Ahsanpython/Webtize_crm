# from django.contrib import admin
# from .models import Expense

# @admin.register(Expense)
# class ExpenseAdmin(admin.ModelAdmin):
#     list_display = ('date','category','amount','vendor','payment_method','client','project')
#     list_filter = ('category','payment_method','date')
#     search_fields = ('description','vendor')
#     date_hierarchy = 'date'

from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'vendor', 'payment_method')  # removed client/project
    list_filter = ('category', 'payment_method', 'date')
    search_fields = ('description', 'vendor')
    date_hierarchy = 'date'

    # Hide fields in the admin form
    fields = ('date', 'category', 'description', 'amount', 'vendor', 'payment_method')
