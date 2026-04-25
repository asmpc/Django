from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from config.models import BaseModel
from task_manager.managers import TaskManager




class TaskStatus(models.TextChoices):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    FAILED = 'failed'


class Tasks(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
        verbose_name= "Наименование",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    status = models.CharField(
        choices=TaskStatus,
        default = TaskStatus.CREATED,
        verbose_name="Статус",
    )
    priority = models.IntegerField(
        validators=[
        MinValueValidator(1),
        MaxValueValidator(5)],
        default=3,
        verbose_name="Приоритетность",
    )
    is_reopen = models.BooleanField(
        verbose_name="Переоткрывалась ли",
        default=False,
    )

    project = models.ForeignKey(
        to = "Projects",
        related_name="tasks",
        verbose_name="Проект",
        on_delete=models.CASCADE,
        null=True,
    )

    assignee = models.ForeignKey(
        to="account.User",
        related_name="tasks",
        on_delete=models.SET_NULL,
        verbose_name="Исполнитель",
        null=True,
        blank=True,
    )

    objects = TaskManager()

    class Meta:
        ordering = [ "-created_at", "name"]
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name

# для встройки в кастомный менеджер
# class CompletedTasksManager(models.Manager):
#     def get_queryset(self):
#         return Tasks.objects.filter(status=TaskStatus.COMPLETED)


# Кастомный менеджер + поиск всех completed - EducationTasks.completed.all()
class EducationTasks(Tasks):
    class CompletedTasksManager(models.Manager):
        def get_queryset(self):
            return Tasks.objects.filter(status=TaskStatus.COMPLETED)

    completed = CompletedTasksManager()
    class Meta:
        proxy = True