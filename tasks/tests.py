from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from projects.models import Project
from tasks.models import Task

User = get_user_model()


class TasksViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.project1 = Project.objects.create(name="Project 1", owner=self.user1)
        self.project2 = Project.objects.create(name="Project 2", owner=self.user2)

        self.task = Task.objects.create(
            name="Task 1", owner=self.user1, project=self.project1
        )

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
            reverse(
                "tasks", kwargs={"project_id": "00000000-0000-0000-0000-000000000000"}
            )
        )
        self.assertEqual(response.status_code, 404)
