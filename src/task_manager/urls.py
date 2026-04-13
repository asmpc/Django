
from django.urls import path, re_path
from task_manager.views import (index,task, user,
                                urequest, create_task_form, create_comment_form,
                                create_tag_form, create_attachment_form, attachments)

urlpatterns = [
    path('', index, name='home'),
    path('tasks', task, name='task'),
    path('users', user, name='user'),
    path('users/<int:user_id>/', urequest, name='urequest'),
    path('create', create_task_form, name='create_task'),
    path('comment', create_comment_form, name='create_comment'),
    path('tag', create_tag_form, name='create_tag'),
    path('attachment', create_attachment_form, name='create_attachment'),
    path('attachments', attachments, name='attachments'),
]