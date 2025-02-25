from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()


class ProjectsViewTests(TestCase):
    def setUp(self):
        """Set up test user and sample projects"""
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        self.project = Project.objects.create(name="Test Project", owner=self.user)
        self.url = reverse("projects")

    def test_get_projects(self):
        """Test GET method returns user's projects"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), [{"id": str(self.project.id), "name": self.project.name}]
        )

    def test_post_project_success(self):
        """Test POST method successfully creates a new project"""
        response = self.client.post(self.url, {"name": "New Project"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 2)

    def test_post_project_empty_name(self):
        """Test POST method returns 400 if name is empty"""
        response = self.client.post(self.url, {"name": " "})
        self.assertEqual(response.status_code, 400)
        self.assertIn("The project name cannot be empty", response.json()["error"])
