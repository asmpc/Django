from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import post_save

class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'
    verbose_name = "Менеджер задач"

    # объявляем для работы signal при создании задач
    # def ready(self):
    #     from task_manager.signals import create_tasks_signal

