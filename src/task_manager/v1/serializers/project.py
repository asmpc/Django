from rest_framework import serializers
from task_manager.models import Projects


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ["id", "name", "description", "owner",]