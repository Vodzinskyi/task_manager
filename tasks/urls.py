from django.urls import path
from .views import TasksView, TaskDetailView

urlpatterns = [
    path("", TasksView.as_view(), name="tasks"),
    path("<uuid:pk>/", TaskDetailView.as_view(), name="task_detail"),
]
