from django.shortcuts import render

from django.http import HttpResponse

from task_manager.models import Tasks

# MTV
def index(request):
    return render (request,"home.html")

def user(request):

    users = [
        {"name": "Alice", "age": 25, "photo": "female1.jpg"},
        {"name": "Bob", "age": 30, "photo": "male1.jpg"},
        {"name": "Jane", "age": 22, "photo": "female2.jpg"},
        {"name": "Charlie", "age": 28, "photo": "male2.jpg"},
        {"name": "Diana", "age": 22, "photo": "female3.jpg"}
    ]

    context = {
        'users': users
    }
    return render (request,"users.html", context=context)

def task(request):

    context = {
        'tasks': Tasks.objects.all().order_by('id')
    }
    return render (request,"tasks.html", context=context)