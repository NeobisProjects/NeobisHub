from django.contrib import admin

from project.models import Project, Screenshot, Document, UserProject


class DocumentInline(admin.StackedInline):
    model = Document
    extra = 1


class ScreenshotInline(admin.StackedInline):
    model = Screenshot
    extra = 2


class UserProjectInline(admin.StackedInline):
    model = UserProject
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [DocumentInline, ScreenshotInline, UserProjectInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Screenshot)
admin.site.register(Document)
