from django.contrib import admin

from department.models import Department
from user_profile.admin import UserProfileInline


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline, ]


admin.site.register(Department, DepartmentAdmin)
