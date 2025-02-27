from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from projects.models import Project
from tasks.models import Task


class TaskService:
    @staticmethod
    def update_task(user, task_id, project_id, data):
        """Updates task if the user is the owner of the project."""
        project = get_object_or_404(Project, id=project_id)
        if project.owner != user:
            raise PermissionDenied("You don't have permission to update this task.")

        task = get_object_or_404(Task, id=task_id, project=project)

        allowed_fields = {
            "name": TaskService._update_name,
            "is_completed": TaskService._update_is_completed,
            # "deadline": TaskService._update_deadline,
            # "position": TaskService._update_position
        }

        updated = False
        for field, update_func in allowed_fields.items():
            if field in data:
                update_func(task, data)
                updated = True

        if updated:
            task.save()

    @staticmethod
    def delete_task(user, task_id, project_id):
        """Deletes a task if the user is the owner of the project."""
        project = get_object_or_404(Project, id=project_id)
        if project.owner != user:
            raise PermissionDenied("You don't have permission to delete this task.")

        task = get_object_or_404(Task, id=task_id, project=project)
        task.delete()

    @staticmethod
    def _update_name(task, data):
        name = data.get("name", "").strip()
        if not name:
            raise ValueError("Task name is required.")
        task.name = name

    @staticmethod
    def _update_is_completed(task, data):
        is_completed = {"true": True, "false": False}.get(
            data.get("is_completed").lower(), None
        )
        task.is_completed = is_completed
