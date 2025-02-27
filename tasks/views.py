from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from projects.models import Project
from tasks.models import Task
from tasks.services import TaskService


class TasksView(LoginRequiredMixin, View):
    """Handles retrieving and creating tasks for a specified project."""

    def get(self, request, project_id):
        """Retrieves user's tasks for the specified project."""
        project = get_object_or_404(Project, id=project_id)
        if project.owner != request.user:
            return HttpResponseForbidden(
                "You don't have permission to access this project."
            )

        tasks = Task.objects.filter(project=project).values("id", "name")
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
            new_task = Task.objects.create(name=name, project=project)
            return JsonResponse({"id": new_task.id, "name": new_task.name}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class TaskDetailView(LoginRequiredMixin, View):
    def patch(self, request, pk, project_id):
        pass

    def delete(self, request, pk, project_id):
        """Deletes a task if the requesting user is the owner of the project."""
        try:
            TaskService.delete_task(request.user, pk, project_id)
            return HttpResponse(status=204)
        except PermissionDenied:
            return HttpResponseForbidden(
                "You don't have permission to modify this project."
            )
