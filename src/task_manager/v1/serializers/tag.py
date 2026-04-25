from rest_framework import serializers
from task_manager.models import Tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "name", ] # "tasks",