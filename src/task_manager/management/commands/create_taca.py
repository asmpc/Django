# Создаем задачу и несколько комментариев в одной транзакции (с откатом при ошибке)

import random
from random import choices
from itertools import islice

from django.core.management.base import BaseCommand

from account.models import User
from task_manager.models import Tasks, Projects, Comments, Tags
from task_manager.models.tasks import TaskStatus
from faker import Faker
from django.db import transaction

fake = Faker(['en_US'])

class Command(BaseCommand):
    # @transaction.atomic
    def handle(self, *args, **kwargs):
        # либо так
        with transaction.atomic():

            users = User.objects.all()
            projects = Projects.objects.all()

            task=Tasks(
                name=fake.text(max_nb_chars=30),
                description=fake.text(max_nb_chars=200),
                assignee=random.choice(users),
                project=random.choice(projects),
                priority=random.choice(choices(range(1,6))),
                status=random.choice(TaskStatus.values),
            )

            # добавил для отработки валидатора модели (валидатор по приоритету)
            task.full_clean()

            task.save()

            # вызываем ошибку для теста транзакции
            raise ValueError

            task = Tasks.objects.latest("created_at")
            users = User.objects.all()
            comments = []

            for _ in range(random.randint(1, 3)):
                comments.append(
                    Comments(
                        message=fake.text(max_nb_chars=50),
                        user=random.choice(users),
                        task=task
                    )
                )

            Comments.objects.bulk_create(comments)





