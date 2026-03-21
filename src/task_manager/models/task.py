from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TaskStatus(models.TextChoices):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    FAILED = 'failed'


class Tasks(models.Model):
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        ordering = ["-priority", "-created_at"]
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name