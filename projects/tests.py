import uuid
from urllib.parse import urlencode

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


class ProjectDetailViewTests(TestCase):
    def setUp(self):
        """Set up test user and sample projects"""
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.client.login(username="user1", password="password")

        self.project1 = Project.objects.create(name="Project1", owner=self.user1)
        self.project2 = Project.objects.create(name="Project2", owner=self.user2)

        self.url1 = reverse("project_detail", kwargs={"pk": self.project1.id})
        self.url2 = reverse("project_detail", kwargs={"pk": self.project2.id})

    def test_patch_project_success(self):
        """Test PATCH successfully updates the project name"""
        response = self.client.patch(
            self.url1,
            data=urlencode({"name": "Updated Project"}),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 200)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, "Updated Project")

    def test_patch_project_empty_name(self):
        """Test PATCH returns 400 if the name is empty"""
        response = self.client.patch(
            self.url1,
            data=urlencode({"name": ""}),
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "The project name cannot be empty")

    def test_patch_project_not_owner(self):
        """Test PATCH returns 403 if user is not the owner"""
        response = self.client.patch(
            self.url2,
            data={"name": "Hacked Name"},
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 403)
        self.project2.refresh_from_db()
        self.assertNotEqual(self.project2.name, "Hacked Name")

    def test_delete_project_success(self):
        """Test DELETE method successfully deletes the project"""
        response = self.client.delete(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(id=self.project1.id).exists())

    def test_delete_project_not_owner(self):
        """Test DELETE method returns 403 if user is not the owner"""
        response = self.client.delete(self.url2)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(id=self.project2.id).exists())

    def test_delete_nonexistent_project(self):
        """Test DELETE method returns 404 if project does not exist"""
        nonexistent_url = reverse("project_detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.delete(nonexistent_url)
        self.assertEqual(response.status_code, 404)
