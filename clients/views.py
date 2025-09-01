
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Client

class ClientListView(ListView):
    model = Client
    template_name = "clients/list.html"
    context_object_name = "clients"

class ClientCreateView(CreateView):
    model = Client
    fields = ["name","organization","email","phone","address","notes"]
    success_url = reverse_lazy("client_list")
    template_name = "clients/form.html"
