
from django.contrib import admin
from .models import Invoice, InvoiceItem
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number","client","project","issue_date","due_date","status","total","paid_amount")
    list_filter = ("status","issue_date","due_date")
    search_fields = ("number","client__name","project__name")
    inlines = [InvoiceItemInline]
@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("invoice","description","quantity","unit_price")
