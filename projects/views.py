from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, QueryDict
from django.shortcuts import get_object_or_404
from django.views import View

from projects.models import Project


class ProjectsView(LoginRequiredMixin, View):
    """Handles retrieving and creating projects for the logged-in user."""

    def get(self, request):
        """Returns a list of projects belonging to the authenticated user."""
        lists = Project.objects.filter(owner=request.user).values("id", "name")
        return JsonResponse(list(lists), safe=False)

    def post(self, request):
        """Creates a new project if the provided name is valid."""
        name = request.POST.get("name", "").strip()
        if not name:
            return JsonResponse(
                {"error": "The project name cannot be empty"}, status=400
            )
        try:
            new_project = Project.objects.create(name=name, owner=request.user)
            return JsonResponse(
                {"id": new_project.id, "name": new_project.name}, status=201
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class ProjectDetailView(LoginRequiredMixin, View):
    """Handles operations on a specific project."""

    def patch(self, request, pk):
        """Update a project name"""
        project = get_object_or_404(Project, id=pk)
        if project.owner != request.user:
            return HttpResponseForbidden()
        data = QueryDict(request.body.decode())
        name = data.get("name").strip()
        if not name:
            return JsonResponse(
                {"error": "The project name cannot be empty"}, status=400
            )
        if name == project.name:
            return JsonResponse(
                {"message": "The project name is already current"}, status=200
            )
        project.name = name
        project.save()
        return HttpResponse(status=200)

    def delete(self, request, pk):
        """Deletes a project if the requesting user is the owner."""
        project = get_object_or_404(Project, id=pk)
        if project.owner != request.user:
            return HttpResponseForbidden()
        project.delete()
        return HttpResponse(status=200)
