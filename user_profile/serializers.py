from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from user_profile.models import UserProfile

User = get_user_model()


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
    resume = serializers.FileField()

    class Meta:
        model = User
        fields = ('email', 'password', 'password_repeat', 'name', 'department',
                  'phone', 'telegram', 'status', 'congestion', 'validation_code', 'resume',)

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)

        if self.validated_data['password'] != self.validated_data['password_repeat']:
            raise serializers.ValidationError(detail='Ваши пароли не совпадают')
        return is_valid


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'department', 'phone', 'telegram', 'status', 'congestion', 'validation_code', 'resume ')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name', 'department', 'phone', 'telegram', 'status', 'congestion', 'validation_code', 'resume ')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'password')
