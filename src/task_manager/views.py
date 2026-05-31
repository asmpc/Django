from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import caches
from django.core.cache import cache
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView

from task_manager.models import Tasks, Comments, Attachments, Tags
from account.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.core.paginator import Paginator, EmptyPage

from .forms import TaskForm, CommentForm, TagForm, AttachmentForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from task_manager.tasks import (
    send_user_comments_email,
    count_user_comments,
)



# MTV

# def index(request):
#     return render (request,"home.html")

# Используем TemplateView для отображения home.html
class HomePage(TemplateView):
    template_name = "home.html"

# добавил кэширование qweryset
# Используем ListView для отображения tasks.html
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TasksPage(PermissionRequiredMixin, ListView):
    model = Tasks
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 10

    # проверка пермиссий используя миксин
    permission_required = "task_manager.view_tasks"

    def get_queryset(self):
        cache_key = "tasks_all"

        tasks = cache.get(cache_key)

        if tasks is None:
            tasks = Tasks.objects.task_optimization()
            cache.set(cache_key, tasks, 60 * 10)

        return tasks



    # без кэш для auth
    # def get_queryset(self):
    #     return Tasks.objects.task_optimization()

        # до подключения кастомного менеджера

        # return (Tasks.objects.select_related("assignee", "project")
        #         .prefetch_related("tags", "comments")
        #         .all().order_by( '-created_at'))


# @permission_required("task_manager.view_tasks")
# def task(request):
#
#     # создаем видимость нагрузки
#     # import time
#     # time.sleep(5)
#
#     tasks_qs = (Tasks.objects.select_related("assignee", "project")
#                 .prefetch_related("tags", "comments")
#                 .all().order_by( '-created_at')) #'name',
#     paginator = Paginator(tasks_qs, 10)
#     page_number = request.GET.get('page')
#     page_objc = paginator.get_page(page_number)
#
#     context = {
#         'tasks': page_objc,
#         'page_obj': page_objc
#     }
#
#     return render(request, "tasks.html", context=context)

    # использовалось до пагинации
    # context = {
    #     'tasks': Tasks.objects.select_related("assignee", "project").prefetch_related("tags", "comments").all().order_by('-created_at')
    # }
    # return render (request,"tasks.html", context=context)


# Используем ListView для отображения users.html
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UserPage(PermissionRequiredMixin, ListView):
    model = User
    template_name = "users.html"
    context_object_name = "users"
    paginate_by = 10

    # проверка пермиссий используя миксин
    permission_required = "account.view_user"


    def get_queryset(self):
        return User.objects.all().order_by('id')


# def user(request):
#
#     users_qs = User.objects.all().order_by('id')
#     paginator = Paginator(users_qs, 10)
#     page_number = request.GET.get('page')
#     page_objc = paginator.get_page(page_number)
#
#     context = {
#         'users': page_objc,
#         'page_obj': page_objc
#     }
#
#     return render (request,"users.html", context=context)


# @method_decorator(cache_page(timeout=60 * 30, cache="database_cache"), name="dispatch")
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AttachmentsPage(PermissionRequiredMixin, ListView):
    model = Attachments
    template_name = "attachments.html"
    context_object_name = "attachments"
    paginate_by = 10

    # проверка пермиссий используя миксин
    permission_required = "task_manager.view_attachments"

    # корректно кэш с аутентификацией
    def get_queryset(self):
        cache_key = "attachments_all"

        attachments = cache.get(cache_key)

        if attachments  is None:
            attachments = Attachments.objects.attachment_optimization()
            cache.set(cache_key, attachments, 60 * 10)

        return attachments



    # def get_queryset(self):
    #     return Attachments.objects.attachment_optimization()

        # return Attachments.objects.select_related('task').all().order_by('id')


# # кэшируем вьюшку на 30 минут используя кэш базы данных
# @cache_page(60 * 30, cache="database_cache")
# def attachments(request):
#
#     attachments_qs = Attachments.objects.select_related('task').all().order_by('id')
#     paginator = Paginator(attachments_qs, 10)
#     page_number = request.GET.get('page')
#     page_objc = paginator.get_page(page_number)
#
#     context = {
#         'attachments': page_objc,
#         'page_obj': page_objc
#     }
#
#     return render (request,"attachments.html", context=context)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UrequestPage(PermissionRequiredMixin, DetailView):
    model = User
    template_name = "urequest.html"
    context_object_name = "user"

    # проверка пермиссий используя миксин
    permission_required = "account.view_user"

    def get_queryset(self):
        return User.objects.prefetch_related('comments__task')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)

        send_user_comments_email.delay(user.id)
        count_user_comments.delay(user.id)

        return user


# def urequest(request, user_id):
#
#     # user = User.objects.get(id=user_id)
#     # вариант выпадения в стандартную ошибку 404 в случае если не найден пользователь
#     # user = get_object_or_404(User, id=user_id)
#     user_qs = User.objects.prefetch_related('comments__task')
#     user = get_object_or_404(user_qs, id=user_id)
#
#     context = {
#         'user': user,
#     }
#     return render (request,"urequest.html", context=context)


class CreateTask(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = "task_form.html"
    model = Tasks
    form_class = TaskForm
    success_url = reverse_lazy("task")

    # проверка пермиссий используя миксин
    permission_required = "task_manager.add_tasks"

    def form_valid(self, form):
        # сохраняем задачу
        response = super().form_valid(form)
        # уже сохраненнная задача
        task = self.object
        # получаем админа
        user = User.objects.get(email="admin@admin.ru")
        # создаём комментарий
        Comments.objects.create(
            task=task,
            message="Task created",
            user=user
        )

        #  чистим кэш корректно
        cache.delete("tasks_all")

        # очистка всех кешей
        # for cache in caches.all():
        #     cache.clear()

        return response

# def create_task_form(request):
#     # import pdb;pdb.set_trace()
#
#     if request.method == "POST":
#
#         form = TaskForm(request.POST)
#
#         if form.is_valid():
#
#             # варианты для формы не связанной с моделью
#             # Tasks.objects.create(
#             #     name=form.cleaned_data['name'],
#             #     priority=form.cleaned_data['priority']
#             # )
#             # или так
#             # Tasks.objects.create(
#             #     name=request.POST['name'],
#             #     priority=request.POST['priority']
#             # )
#
#             # для формы связанной с моделью
#             # form.save()
#
#             # Не используя сигнал, создаем к каждой задаче комментарий
#             task = form.save()
#
#             # Создаем коммент от admin при создании новой задачи
#             user = User.objects.get(email="admin@admin.ru")
#
#             Comments.objects.create(
#                 task=task,
#                 message="Task created",
#                 user=user
#             )
#
#             # Инвалидация кэша после создания задачи
#             for cache in caches.all():
#                 cache.clear()
#
#             return HttpResponseRedirect(reverse("task"))
#     else:
#         form = TaskForm()
#
#     return render(request, "task_form.html", {"form": form})


class CreateComment(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'comment_form.html'
    model = Comments
    form_class = CommentForm
    success_url = reverse_lazy("task")

    # проверка пермиссий используя миксин
    permission_required = 'task_manager.add_comments'

    def form_valid(self, form):
        response = super().form_valid(form)


        #  чистим кэш корректно
        cache.delete("tasks_all")

        # очистка всех кешей
        # for cache in caches.all():
        #     cache.clear()

        return response


# def create_comment_form(request):
#     # import pdb;pdb.set_trace()
#
#     if request.method == "POST":
#
#         form = CommentForm(request.POST)
#
#         if form.is_valid():
#
#             form.save()
#
#
#             caches["default"].clear()
#             caches["database_cache"].clear()
#
#             return HttpResponseRedirect(reverse("task"))
#     else:
#         form = CommentForm()
#
#     return render(request, "comment_form.html", {"form": form})


class CreateTag(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'tag_form.html'
    model = Tags
    form_class = TagForm
    success_url = reverse_lazy("task")

    # проверка пермиссий используя миксин
    permission_required = "task_manager.add_tags"

    def form_valid(self, form):
        response = super().form_valid(form)


        #  чистим кэш корректно
        cache.delete("tasks_all")


        # очистка всех кешей
        # for cache in caches.all():
        #     cache.clear()

        return response



# def create_tag_form(request):
#
#     if request.method == "POST":
#
#         form = TagForm(request.POST)
#
#         if form.is_valid():
#
#             instance = form.save(commit=False)
#             instance.save()
#             form.save_m2m()
#
#             for cache in caches.all():
#                 cache.clear()
#
#             return HttpResponseRedirect(reverse("task"))
#     else:
#         form = TagForm()
#
#     return render(request, "tag_form.html", {"form": form})


class CreateAttachment(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'attachment_form.html'
    model = Attachments
    form_class = AttachmentForm
    success_url = reverse_lazy("task")

    # проверка пермиссий используя миксин
    permission_required = "task_manager.add_attachments"

    def form_valid(self, form):
        response = super().form_valid(form)

        #  чистим кэш корректно
        cache.delete("attachments_all")

        # очистка всех кешей
        # for cache in caches.all():
        #     cache.clear()

        return response

# def create_attachment_form(request):
#
#     if request.method == "POST":
#
#         form = AttachmentForm(request.POST, request.FILES)
#
#         if form.is_valid():
#
#             form.save()
#
#             for cache in caches.all():
#                 cache.clear()
#
#             return HttpResponseRedirect(reverse("task"))
#     else:
#         form = AttachmentForm()
#
#     return render(request, "attachment_form.html", {"form": form})

class DeleteCommentPage(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Comments
    template_name = "comment_delete.html"

    # проверка пермиссий используя миксин
    permission_required = "task_manager.delete_comments"

    def get_success_url(self):
        return reverse_lazy(
            "urequest",
            kwargs={"pk": self.object.user_id}
        )