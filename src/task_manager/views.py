from django.http import HttpResponse

from task_manager.models import Tasks, Comments, Attachments
from account.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.core.paginator import Paginator, EmptyPage

from .forms import TaskForm, CommentForm, TagForm, AttachmentForm



# MTV
def index(request):
    return render (request,"home.html")

def user(request):

    users_qs = User.objects.all().order_by('id')
    paginator = Paginator(users_qs, 10)
    page_number = request.GET.get('page')
    page_objc = paginator.get_page(page_number)

    context = {
        'users': page_objc,
        'page_obj': page_objc
    }

    return render (request,"users.html", context=context)

def attachments(request):

    attachments_qs = Attachments.objects.all().order_by('id')
    paginator = Paginator(attachments_qs, 10)
    page_number = request.GET.get('page')
    page_objc = paginator.get_page(page_number)

    context = {
        'attachments': page_objc,
        'page_obj': page_objc
    }

    return render (request,"attachments.html", context=context)


def urequest(request, user_id):

    # user = User.objects.get(id=user_id)
    # вариант выпадения в стандартную ошибку 404 в случае если не найден пользователь
    # user = get_object_or_404(User, id=user_id)
    user_qs = User.objects.prefetch_related('comments__task')
    user = get_object_or_404(user_qs, id=user_id)

    context = {
        'user': user,
    }
    return render (request,"urequest.html", context=context)


def task(request):
    tasks_qs = (Tasks.objects.select_related("assignee", "project")
                .prefetch_related("tags", "comments")
                .all().order_by('name', '-created_at')) #'name',
    paginator = Paginator(tasks_qs, 10)
    page_number = request.GET.get('page')
    page_objc = paginator.get_page(page_number)

    context = {
        'tasks': page_objc,
        'page_obj': page_objc
    }

    return render(request, "tasks.html", context=context)

    # использовалось до пагинации
    # context = {
    #     'tasks': Tasks.objects.select_related("assignee", "project").prefetch_related("tags", "comments").all().order_by('-created_at')
    # }
    # return render (request,"tasks.html", context=context)


def create_task_form(request):
    # import pdb;pdb.set_trace()

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            # варианты для формы не связанной с моделью
            # Tasks.objects.create(
            #     name=form.cleaned_data['name'],
            #     priority=form.cleaned_data['priority']
            # )
            # или так
            # Tasks.objects.create(
            #     name=request.POST['name'],
            #     priority=request.POST['priority']
            # )

            # для формы связанной с моделью
            # form.save()

            # Не используя сигнал, создаем к каждой задаче комментарий
            task = form.save()

            user = User.objects.get(email="admin@admin.ru")

            Comments.objects.create(
                task=task,
                message="Task created",
                user=user
            )

            return HttpResponseRedirect(reverse("task"))
    else:
        form = TaskForm()

    return render(request, "task_form.html", {"form": form})

def create_comment_form(request):
    # import pdb;pdb.set_trace()

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("task"))
    else:
        form = CommentForm()

    return render(request, "comment_form.html", {"form": form})

def create_tag_form(request):

    if request.method == "POST":

        form = TagForm(request.POST)

        if form.is_valid():

            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("task"))
    else:
        form = TagForm()

    return render(request, "tag_form.html", {"form": form})

def create_attachment_form(request):

    if request.method == "POST":

        form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse("task"))
    else:
        form = AttachmentForm()

    return render(request, "attachment_form.html", {"form": form})