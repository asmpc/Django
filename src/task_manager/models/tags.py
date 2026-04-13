from django.db import models


from config.models import BaseModel



class Tags(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Наименование",
    )
    tasks = models.ManyToManyField(
        to='Tasks',
        related_name="tags",
        verbose_name="Задачи",
    )

    class Meta:
        ordering = ["-created_at"]
        db_table = "tags"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name