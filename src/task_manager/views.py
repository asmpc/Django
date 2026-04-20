from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import caches
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView

from task_manager.models import Tasks, Comments, Attachments, Tags
from account.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.core.paginator import Paginator, EmptyPage

from .forms import TaskForm, CommentForm, TagForm, AttachmentForm



# MTV

# def index(request):
#     return render (request,"home.html")

# Используем TemplateView для отображения home.html
class HomePage(TemplateView):
    template_name = "home.html"


# Используем ListView для отображения tasks.html
class TasksPage(ListView):
    model = Tasks
    template_name = "tasks.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        return (Tasks.objects.select_related("assignee", "project")
                .prefetch_related("tags", "comments")
                .all().order_by( '-created_at'))



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
class UserPage(ListView):
    model = User
    template_name = "users.html"
    context_object_name = "users"
    paginate_by = 10

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

@method_decorator(cache_page(timeout=60 * 30, cache="database_cache"), name="dispatch")
class AttachmentsPage(ListView):
    model = Attachments
    template_name = "attachments.html"
    context_object_name = "attachments"
    paginate_by = 10
    def get_queryset(self):
        return Attachments.objects.select_related('task').all().order_by('id')


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


class UrequestPage(DetailView):
    model = User
    template_name = "urequest.html"
    context_object_name = "user"

    def get_queryset(self):
        return User.objects.prefetch_related('comments__task')


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


class CreateTask(CreateView):
    template_name = "task_form.html"
    model = Tasks
    form_class = TaskForm
    success_url = reverse_lazy("task")

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
        # чистим кэш
        for cache in caches.all():
            cache.clear()

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


class CreateComment(CreateView):
    template_name = 'comment_form.html'
    model = Comments
    form_class = CommentForm
    success_url = reverse_lazy("task")

    def form_valid(self, form):
        response = super().form_valid(form)

        # очистка всех кешей
        for cache in caches.all():
            cache.clear()

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


class CreateTag(CreateView):
    template_name = 'tag_form.html'
    model = Tags
    form_class = TagForm
    success_url = reverse_lazy("task")

    def form_valid(self, form):
        response = super().form_valid(form)

        # очистка всех кешей
        for cache in caches.all():
            cache.clear()

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


class CreateAttachment(CreateView):
    template_name = 'attachment_form.html'
    model = Attachments
    form_class = AttachmentForm
    success_url = reverse_lazy("task")

    def form_valid(self, form):
        response = super().form_valid(form)

        # очистка всех кешей
        for cache in caches.all():
            cache.clear()

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

class DeleteCommentPage(DeleteView):
    model = Comments
    template_name = "comment_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "urequest",
            kwargs={"pk": self.object.user_id}
        )