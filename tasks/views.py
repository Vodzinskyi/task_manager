from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views import View

from projects.models import Project
from tasks.models import Task


class TasksView(LoginRequiredMixin, View):
    """Handles retrieving and creating tasks for a specified project."""

    def get(self, request, project_id):
        """Retrieves user's tasks for the specified project."""
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            return HttpResponseForbidden(
                "You don't have permission to access this project."
            )

        tasks = Task.objects.filter(owner=request.user, project=project).values(
            "id", "name"
        )
        return JsonResponse(list(tasks), safe=False)

    def post(self, request, project_id):
        """Creates a new task if the provided name is valid."""
        name = request.POST.get("name", "").strip()
        if not name:
            return JsonResponse({"error": "The task name cannot be empty"}, status=400)

        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            return HttpResponseForbidden(
                "You don't have permission to modify this project."
            )

        try:
            new_task = Task.objects.create(
                name=name, owner=request.user, project=project
            )
            return JsonResponse({"id": new_task.id, "name": new_task.name}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
