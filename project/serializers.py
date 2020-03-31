from rest_framework import serializers

from project.models import Screenshot, Document, Project
from user_profile.serializers import UserProjectSerializer, UserProfileNameAndSurnameSerializer


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ('id', 'image',)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'file',)


class ProjectSerializer(serializers.ModelSerializer):
    team = UserProjectSerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)
    screenshots = ScreenshotSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'logo', 'date_of_start', 'date_of_finish', 'pm', 'team',
                  'description', 'product_owner', 'status', 'documents', 'screenshots',)


class ListProjectSerializer(serializers.ModelSerializer):
    pm = UserProfileNameAndSurnameSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'pm', 'description', 'status',)
