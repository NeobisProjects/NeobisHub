from rest_framework import generics

from department.models import Department
from department.serializers import DepartmentSerializer


class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()


class DepartmentRetrieveView(generics.RetrieveAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
