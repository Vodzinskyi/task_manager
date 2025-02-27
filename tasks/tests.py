import uuid

from django.core.exceptions import PermissionDenied
from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task
from tasks.services import TaskService

User = get_user_model()


class TasksViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.project1 = Project.objects.create(name="Project 1", owner=self.user1)
        self.project2 = Project.objects.create(name="Project 2", owner=self.user2)

        self.task = Task.objects.create(name="Task 1", project=self.project1)

        self.client.login(username="user1", password="password")

    def test_get_tasks_success(self):
        """User can retrieve tasks for their project."""
        response = self.client.get(
            reverse("tasks", kwargs={"project_id": self.project1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), [{"id": str(self.task.id), "name": self.task.name}]
        )

    def test_get_tasks_forbidden(self):
        """User cannot retrieve tasks for another user's project."""
        response = self.client.get(
            reverse("tasks", kwargs={"project_id": self.project2.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_create_task_success(self):
        """User can create a task in their project."""
        response = self.client.post(
            reverse("tasks", kwargs={"project_id": self.project1.id}),
            {"name": "New Task"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.filter(project=self.project1).count(), 2)

    def test_create_task_empty_name(self):
        """Creating a task with an empty name should return 400."""
        response = self.client.post(
            reverse("tasks", kwargs={"project_id": self.project1.id}), {"name": ""}
        )
        self.assertEqual(response.status_code, 400)

    def test_create_task_forbidden(self):
        """User cannot create a task in another user's project."""
        response = self.client.post(
            reverse("tasks", kwargs={"project_id": self.project2.id}),
            {"name": "Hacked Task"},
        )
        self.assertEqual(response.status_code, 403)

    def test_get_tasks_not_found(self):
        """Requesting tasks for a non-existent project should return 404."""
        response = self.client.get(
            reverse("tasks", kwargs={"project_id": uuid.uuid4()})
        )
        self.assertEqual(response.status_code, 404)


class TaskServiceDeleteTest(TestCase):
    def setUp(self):
        """Create test users, project, and task."""
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.project = Project.objects.create(name="Test Project", owner=self.user1)
        self.task = Task.objects.create(name="Test Task", project=self.project)

    def test_delete_task_success(self):
        """Owner can delete their task."""
        TaskService.delete_task(self.user1, self.task.id, self.project.id)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_permission_denied(self):
        """Non-owner cannot delete the task."""
        with self.assertRaises(PermissionDenied):
            TaskService.delete_task(self.user2, self.task.id, self.project.id)

    def test_delete_nonexistent_task(self):
        """Deleting a non-existent task raises an error."""
        with self.assertRaisesMessage(Exception, "No Task matches the given query."):
            TaskService.delete_task(self.user1, uuid.uuid4(), self.project.id)

    def test_update_task_permission_denied(self):
        """Non-owner cannot update the task name."""
        data = QueryDict("name=Unauthorized Update")
        with self.assertRaises(PermissionDenied):
            TaskService.update_task(self.user2, self.task.id, self.project.id, data)

    def test_update_task_name_success(self):
        """Owner can update task name."""
        data = QueryDict("name=Updated Task Name")
        TaskService.update_task(self.user1, self.task.id, self.project.id, data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task Name")

    def test_update_task_name_empty(self):
        """Cannot update task with empty name."""
        data = QueryDict("name=")
        with self.assertRaises(ValueError):
            TaskService.update_task(self.user1, self.task.id, self.project.id, data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Test Task")

    def test_update_task_is_completed(self):
        """Owner can update task completion status."""
        data = QueryDict("is_completed=true")
        TaskService.update_task(self.user1, self.task.id, self.project.id, data)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
