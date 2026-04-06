from django.db import models


from config.models import BaseModel



class Projects(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Наименование",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )

    owner = models.ForeignKey(
        to="account.User",
        related_name="projects",
        verbose_name="Руководитель",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name