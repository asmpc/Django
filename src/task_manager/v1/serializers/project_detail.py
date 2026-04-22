from rest_framework import serializers
from task_manager.models import ProjectDetails


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetails
        fields = ["id", "info", "serial_id", "project",]