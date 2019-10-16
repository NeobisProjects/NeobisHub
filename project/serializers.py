from rest_framework import serializers

from project.models import Screenshot, Document, Project


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ('image', )


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'file', )


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'logo', 'date_of_start', 'date_of_finish', 'team',
                 'product_owner', 'status', 'documents', 'screenshots',)