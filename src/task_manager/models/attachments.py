import os
from django.db import models

from django.contrib import admin
from config.models import BaseModel
from django.utils.html import format_html
from django.core.exceptions import ValidationError


def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError('Файл слишком большой. Максимум 5 МБ.')

def validate_file_type(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError('Разрешены только изображения и PDF файлы.')



class Attachments(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Наименование",
    )

    task = models.ForeignKey(
        to='Tasks',
        related_name="attachments",
        on_delete=models.CASCADE,
        verbose_name="Задача",
    )

    photo = models.ImageField(
        upload_to="attachments/",
        null=True, blank=True,
        validators=[validate_file_size],
        verbose_name="Фото"
    )

    file = models.FileField(
        upload_to="attachments/",
        null=True, blank=True,
        validators=[validate_file_size, validate_file_type],
        verbose_name="Файл"
    )

    class Meta:
        ordering = ["name"]
        db_table = "attachments"
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):

        if self.photo:
            self.photo.delete(save=False)

        if self.file:
            self.file.delete(save=False)

        super().delete(*args, **kwargs)

    @admin.display(description="Превью")
    def preview(self):
        if self.photo:
            return format_html(
                '<img src="{}" style="max-height: 100px;" />',
                self.photo.url
            )

        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()

            if ext == ".pdf":
                return format_html(
                    '<a href="{}" target="_blank">📄 PDF</a>',
                    self.file.url
                )

            return format_html(
                '<a href="{}" target="_blank">📎 Скачать</a>',
                self.file.url
            )

        return "—"