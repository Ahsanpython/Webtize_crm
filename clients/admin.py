
from django.contrib import admin
from .models import Client
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name","organization","email","phone","created_at")
    search_fields = ("name","organization","email","phone")
