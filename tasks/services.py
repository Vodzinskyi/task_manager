from datetime import datetime

from django.db.models import Max
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from projects.models import Project
from tasks.models import Task


class TaskService:
    """Service class for handling task-related operations."""

    @staticmethod
    def create_task(user, name, project_id):
        """Creates a new task"""
        if not name:
            raise ValueError("Task name is required.")
        project = get_object_or_404(Project, id=project_id)
        TaskService._check_project_owner(user, project)

        max_priority = Task.objects.filter(project=project).aggregate(
            max_priority=Max("priority")
        )["max_priority"]
        new_priority = (max_priority or 0) + 1

        new_task = Task.objects.create(
            name=name, project=project, priority=new_priority
        )

        response = model_to_dict(
            new_task, fields=[field.name for field in Task._meta.fields]
        )
        response["id"] = str(new_task.id)

        return response

    @staticmethod
    def update_task(user, task_id, project_id, data):
        """Updates task if the user is the owner of the project."""
        project = get_object_or_404(Project, id=project_id)
        TaskService._check_project_owner(user, project)

        task = get_object_or_404(Task, id=task_id, project=project)

        allowed_fields = {
            "name": TaskService._update_name,
            "is_completed": TaskService._update_is_completed,
            "deadline": TaskService._update_deadline,
            "priority": TaskService._update_priority,
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
        TaskService._check_project_owner(user, project)

        task = get_object_or_404(Task, id=task_id, project=project)
        task.delete()

    @staticmethod
    def _check_project_owner(user, project):
        """Check if the user is the owner of the project."""
        if project.owner != user:
            raise PermissionDenied("You don't have permission to modify this project.")

    @staticmethod
    def _update_name(task, data):
        """Updates the task name"""
        name = data.get("name", "").strip()
        if not name:
            raise ValueError("Task name is required.")
        task.name = name

    @staticmethod
    def _update_is_completed(task, data):
        """Updates the task completion status"""
        is_completed = {"true": True, "false": False}.get(
            data.get("is_completed").lower(), None
        )
        task.is_completed = is_completed

    @staticmethod
    def _update_priority(task, data):
        """Updates the task priority"""
        priority = data.get("priority", 0)
        task.priority = priority

    @staticmethod
    def _update_deadline(task, data):
        """Updates the task deadline"""
        try:
            deadline = datetime.strptime(data.get("deadline", None), "%Y-%m-%d %H:%M")
            task.deadline = deadline
        except ValueError:
            raise ValueError(
                "Invalid deadline format. Expected format: YYYY-MM-DD HH:MM"
            )
