from django.contrib import admin
from django.contrib.auth import get_user_model

from user_profile.models import UserProfile, UserProject, Progress


class UserProjectInline(admin.StackedInline):
    model = UserProject
    extra = 0


class ProgressInline(admin.ModelAdmin):
    model = Progress
    extra = 0


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [ProgressInline, UserProjectInline]


User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile


@admin.register(User)
class User(admin.ModelAdmin):
    inlines = [UserProfileInline]


admin.register(UserProject)
admin.register(Progress)
