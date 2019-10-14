from django.contrib import admin

from user_profile.models import UserProfile, UserProject, Progress


class UserProjectInline(admin.StackedInline):
    model = UserProject
    extra = 0


class ProgressInline(admin.ModelAdmin):
    model = Progress
    extra = 0


class UserProfileAdmin(admin.ModelAdmin):
    inlines = [ProgressInline, UserProjectInline]


admin.register(UserProfile, UserProfileAdmin)
admin.register(UserProject)
admin.register(Progress)
