from django.contrib import admin
from django.contrib.auth import get_user_model

from user_profile.models import UserProfile, Progress
from project.models import UserProject


class UserProjectInline(admin.StackedInline):
    model = UserProject
    extra = 1


class ProgressInline(admin.StackedInline):
    model = Progress
    extra = 1


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [ProgressInline, UserProjectInline]


User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile


@admin.register(User)
class User(admin.ModelAdmin):
    inlines = [UserProfileInline]


admin.site.register(UserProject)
admin.site.register(Progress)
admin.site.register(UserProfile, UserProfileAdmin)
