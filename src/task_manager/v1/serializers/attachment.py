from rest_framework import serializers
from task_manager.models import Attachments


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = ["id", "name", "task", "photo", "file",]