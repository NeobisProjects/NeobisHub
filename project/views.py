from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter

from project.models import Project
from project.serializers import ProjectSerializer, ListProjectSerializer


class ProjectListView(generics.ListAPIView):
    serializer_class = ListProjectSerializer
    queryset = Project.objects.all().order_by('name')
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ProjectListByStatusView(generics.ListAPIView):
    serializer_class = ListProjectSerializer
    queryset = Project.objects.all().order_by('status')
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ProjectListByPMView(generics.ListAPIView):
    serializer_class = ListProjectSerializer
    queryset = Project.objects.all().order_by('pm')
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ProjectCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProjectSerializer


class ProjectUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
