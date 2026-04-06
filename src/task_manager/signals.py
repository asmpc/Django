from django.db.models.signals import post_save
from django.dispatch import receiver
from task_manager.models import Tasks
from account.models import User

# Используя signal создаем каждой новой задаче коммент - Task created

# @receiver(post_save, sender=Tasks)
# def create_tasks_signal(sender, instance, created, **kwargs):
#     # import pdb;pdb.set_trace()
#     if created:
#         user = User.objects.get(email="admin@admin.ru")
#         instance.comments.create(
#             message="Task created",
#             user=user
#         )



