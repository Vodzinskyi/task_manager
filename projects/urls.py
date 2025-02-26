from django.urls import path
from .views import ProjectsView, ProjectDetailView

urlpatterns = [
    path("", ProjectsView.as_view(), name="projects"),
    path("<uuid:pk>/", ProjectDetailView.as_view(), name="project_detail"),
]
