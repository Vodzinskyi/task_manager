from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from projects.models import Project
from tasks.models import Task


class TaskService:
    @staticmethod
    def delete_task(user, task_id, project_id):
        """Deletes a task if the user is the owner of the project."""
        project = get_object_or_404(Project, id=project_id)
        if project.owner != user:
            raise PermissionDenied("You don't have permission to delete this task.")

        task = get_object_or_404(Task, id=task_id, project=project)
        task.delete()
