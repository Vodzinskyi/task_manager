import uuid

from django.db import models

from projects.models import Project


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name
