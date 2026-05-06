from django_filters import OrderingFilter
from rest_framework import serializers
from task_manager.models import Tasks
from task_manager.v1.serializers.comment import CommentSerializer
import django_filters



# Сериалайзер связанный с моделью

class TaskSerializer(serializers.ModelSerializer):
    is_reopen = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    project = serializers.CharField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Tasks
        fields = ["id", "name", "description",
                  "status", "priority", "is_reopen",
                  "project", "assignee", "comments",
                  ]

    def validate_name(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Task name must be atleast 5 characters")
        return value



class TaskQueryFilterSerializer(django_filters.FilterSet):
    assignee__email = django_filters.CharFilter(
        field_name='assignee__email',
        lookup_expr='iexact',
        label='Assignee email',
        help_text='Filter by exact email of assignee'
    )

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Task name',
        help_text='Case-insensitive search in task name'
    )

    priority = django_filters.NumberFilter(
        field_name='priority',
        label='Priority',
        help_text='Exact priority value'
    )

    priority__gte = django_filters.NumberFilter(
        field_name='priority',
        lookup_expr='gte',
        label='Min priority'
    )

    priority__lte = django_filters.NumberFilter(
        field_name='priority',
        lookup_expr='lte',
        label='Max priority'
    )

    created_at = django_filters.DateFilter(
        field_name='created_at',
        label='Created date',
        help_text='Filter by exact creation date'
    )

    created_at__gte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Created after'
    )

    created_at__lte = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label='Created before'
    )

    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains',
        label='Description contains'
    )

    # сортировка ограничена только этими полями
    ordering = OrderingFilter(
        fields=(
            ('status', 'status'),
            ('priority', 'priority'),
        )
    )

    class Meta:
        model = Tasks
        fields = ['status']



# Сериалайзер не связанный с моделью

# class TaskSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(required=True, allow_blank=False, max_length=100)
#     description = serializers.CharField(required=False, allow_blank=True, max_length=255)
#     priority = serializers.IntegerField()
#
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Task` instance, given the validated data.
#         """
#         return Tasks.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Task instance, given the validated data.
#         """
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get("description", instance.description)
#         instance.priority = validated_data.get("priority", instance.priority)
#         instance.save()
#         return instance