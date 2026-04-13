from django.db import models


from config.models import BaseModel



class Comments(BaseModel):
    message = models.CharField(
        max_length=64,
        unique=False,
        null=False,
        blank=False,
        verbose_name="Текст комментария",
    )

    user = models.ForeignKey(
        to="account.User",
        related_name="comments",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )

    task = models.ForeignKey(
        to="Tasks",
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name="Задача",
    )

    class Meta:
        ordering = ["-created_at", "message"]
        db_table = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.message