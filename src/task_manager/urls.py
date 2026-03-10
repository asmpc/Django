
from django.urls import path
from task_manager.views import index, task, user

urlpatterns = [
    path('', index, name='home'),
    path('tasks', task, name='task'),
    path('users', user, name='user'),

]