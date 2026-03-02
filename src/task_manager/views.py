from django.shortcuts import render

from django.http import HttpResponse

# MTV
def index(request):
    return HttpResponse("<h1>Hello, world. You're at the task_tracker index.</h1>")
