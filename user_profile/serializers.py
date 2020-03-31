from django.contrib.auth import get_user_model
from rest_framework import serializers

from project.models import UserProject
from user_profile.models import UserProfile, Progress

User = get_user_model()


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('id', 'study_plan', 'points', 'out_of')


class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ('id', "user", 'project', 'percentage', 'user_role',)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_repeat = serializers.CharField(required=True)
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    patronymic = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=5)

    class Meta:
        model = User
        fields = ('surname', 'name', 'patronymic', 'status', 'email', 'password', 'password_repeat',)

    def is_valid(self, raise_exception: bool = ...):
        is_valid = super().is_valid(raise_exception)

        if self.validated_data['password'] != self.validated_data['password_repeat']:
            raise serializers.ValidationError(detail='Ваши пароли не совпадают')
        return is_valid


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'surname', 'name', 'patronymic', 'department', 'phone',
                  'telegram', 'status', 'congestion', 'summary',)


class UserProfileRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('surname', 'name', 'patronymic', 'department',
                  'phone', 'telegram', 'status', 'congestion', 'summary',)


class UserProfileSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer()
    project = UserProjectSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'surname', 'name', 'patronymic', 'department', 'phone', 'telegram',
                  'status', 'congestion', 'summary', 'progress', 'project',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileRegistrationSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'profile',)


class UserProfileNameAndSurnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'surname')
