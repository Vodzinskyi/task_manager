from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponse,
    QueryDict,
    HttpResponseBadRequest,
)
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

        tasks = Task.objects.filter(project=project).values()
        return JsonResponse(list(tasks), safe=False)

    def post(self, request, project_id):
        """Creates a new task if the provided name is valid."""
        try:
            name = request.POST.get("name", "").strip()
            response = TaskService.create_task(request.user, name, project_id)
            return JsonResponse(response, status=201)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
        except PermissionDenied as e:
            return HttpResponseForbidden(str(e))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class TaskDetailView(LoginRequiredMixin, View):
    """Handles operations on a specific task."""

    def patch(self, request, pk, project_id):
        """Updates specified fields of a task."""
        try:
            data = QueryDict(request.body.decode())
            TaskService.update_task(request.user, pk, project_id, data)
            return HttpResponse(status=200)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
        except PermissionDenied as e:
            return HttpResponseForbidden(str(e))

    def delete(self, request, pk, project_id):
        """Deletes a task if the requesting user is the owner of the project."""
        try:
            TaskService.delete_task(request.user, pk, project_id)
            return HttpResponse(status=204)
        except PermissionDenied as e:
            return HttpResponseForbidden(str(e))
