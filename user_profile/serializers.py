from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from user_profile.models import UserProfile, Progress, UserProject

User = get_user_model()


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ('study_plan', 'test',)


class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ('project', 'percent_of_project', 'percent_of_user', 'user_role',)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_repeat = serializers.CharField(required=True)
    name = serializers.CharField(max_length=100)
    department = serializers.IntegerField()
    phone = serializers.CharField(max_length=13)
    telegram = serializers.URLField()
    status = serializers.CharField(max_length=5)
    congestion = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    validation_code = serializers.CharField(max_length=6)
    resume = serializers.FileField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_repeat', 'name', 'department',
                  'phone', 'telegram', 'status', 'congestion', 'validation_code', 'resume',)

    def is_valid(self, raise_exception: bool = ...):
        is_valid = super().is_valid(raise_exception)

        if self.validated_data['password'] != self.validated_data['password_repeat']:
            raise serializers.ValidationError(detail='Ваши пароли не совпадают')
        return is_valid


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'department', 'phone', 'telegram', 'status',
                  'congestion', 'validation_code', 'resume ',)


class UserProfileRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('name', 'department', 'phone', 'telegram', 'status', 'congestion', 'validation_code',)


class UserProfileSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer()
    project = UserProjectSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('name', 'department', 'phone', 'telegram', 'status', 'congestion',
                  'validation_code', 'resume ', 'progress', 'project',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileRegistrationSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'profile',)
#TODO:убрать через сериалайзе код при регистрации