from rest_framework import serializers

from department.models import Department
from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer


class ListDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name', )


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name', 'head', 'slack', 'telegram', 'mentor_count',)


class DepartmentWithUserSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(many=True)
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.users.count()

    class Meta:
        model = Department
        fields = ('id', 'head', 'name', 'slack', 'telegram', 'users', 'count', 'mentor_count',)
