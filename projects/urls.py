
from django.urls import path
from . import views
urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
]
