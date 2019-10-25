from django.contrib import admin

from project.models import Project, Screenshot, Document


class DocumentInline(admin.StackedInline):
    model = Document
    extra = 0


class ScreenshotInline(admin.StackedInline):
    model = Screenshot
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [DocumentInline, ScreenshotInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Screenshot)
admin.site.register(Document)
