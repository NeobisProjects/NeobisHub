from rest_framework import generics, permissions

from department.models import Department
from department.serializers import DepartmentSerializer, DepartmentWithUserSerializer, ListDepartmentSerializer


class DepartmentListView(generics.ListAPIView):
    serializer_class = ListDepartmentSerializer
    queryset = Department.objects.all().order_by('name')


class DepartmentRetrieveView(generics.RetrieveDestroyAPIView):
    serializer_class = DepartmentWithUserSerializer
    queryset = Department.objects.all()


class DepartmentCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = DepartmentSerializer


class DepartmentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
