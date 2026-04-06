import random
from random import choices
from itertools import islice

from django.core.management.base import BaseCommand

from account.models import User
from task_manager.models import Tasks, Projects, Comments, Tags
from task_manager.models.tasks import TaskStatus
from faker import Faker
fake = Faker(['en_US'])


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        projects = []
        users = []



        try:
            for _ in range(10):
                projects.append(
                    Projects(
                        name=fake.text(max_nb_chars=20),
                    )
                )
            Projects.objects.bulk_create(projects)

            for _ in range(10):
                users.append(
                    User(
                        email=fake.email(),
                        username=fake.name(),
                        first_name = fake.first_name(),
                        last_name = fake.last_name(),
                        phone=fake.phone_number(),
                    )
                )
            User.objects.bulk_create(users)

            users = User.objects.all()
            projects = Projects.objects.all()

            batch_size = 1000
            objs = (Tasks(
                name=fake.text(max_nb_chars=30),
                description=fake.text(max_nb_chars=200),
                assignee=random.choice(users),
                project=random.choice(projects),
                priority=random.choice(choices(range(1,6))),
                status=random.choice(TaskStatus.values)
            ) for i in range(100000)
            )
            while True:
                batch = list(islice(objs, batch_size))
                if not batch:
                    break
                Tasks.objects.bulk_create(batch, batch_size)

            # for _ in range(1000):
            #     tasks.append(
            #         Tasks(
            #             name=fake.text(max_nb_chars=30),
            #             description=fake.text(max_nb_chars=200),
            #             assignee=random.choice(users),
            #             project=random.choice(projects),
            #             priority=random.choice(choices(range(1,6))),
            #             status=random.choice(TaskStatus.values),
            #         )
            #     )
            # Tasks.objects.bulk_create(tasks)

            tasks = Tasks.objects.all().iterator(chunk_size=1000)

            batch_size = 1000
            comments = []
            for task in tasks:
                for _ in range(random.randint(1, 3)):
                    comments.append(
                        Comments(
                            message=fake.text(max_nb_chars=50),
                            user=random.choice(users),
                            task=task
                        )
                    )
                if len(comments) >= batch_size:
                    Comments.objects.bulk_create(comments)
                    comments.clear()

            if comments:
                Comments.objects.bulk_create(comments)

            # Comments.objects.bulk_create(comments)

            tags = []
            for _ in range(10):
                tags.append(
                    Tags(
                        name=fake.text(max_nb_chars=20),
                    )
                )
            Tags.objects.bulk_create(tags)

            tags = list(Tags.objects.all())

            tasks = Tasks.objects.all().iterator(chunk_size=1000)

            for task in tasks:
                selected_tags = random.choice(tags)
                task.tags.add(selected_tags)

            self.style.SUCCESS('Successfully created tasks')
        except Exception as e:
            self.style.ERROR(f'error is {e}')