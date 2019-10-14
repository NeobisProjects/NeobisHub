from django.contrib import admin

from project.models import Project, Screenshot, Document


class DocumentInline(admin.StackedInline):
    model = Document
    extra = 0


class ScreenshotInline(admin.ModelAdmin):
    model = Screenshot
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [DocumentInline, ScreenshotInline]


admin.register(Project, ProjectAdmin)
admin.register(Screenshot)
admin.register(Document)
