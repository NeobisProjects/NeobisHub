from rest_framework import serializers

from department.models import Department
from user_profile.serializers import UserProfileSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(many=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'users', )
