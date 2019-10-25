from rest_framework import generics

from project.models import Project
from project.serializers import ProjectSerializer


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
