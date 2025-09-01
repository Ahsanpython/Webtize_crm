
from django.urls import path
from . import views
urlpatterns = [
    path("", views.ClientListView.as_view(), name="client_list"),
    path("create/", views.ClientCreateView.as_view(), name="client_create"),
]
