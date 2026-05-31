from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from config.pagination import CustomPagination
from task_manager.models import Tasks
from task_manager.v1.serializers import TaskSerializer
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from task_manager.v1.serializers.task import TaskQueryFilterSerializer
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend



# вручную создаю пагинацию, в generic уже есть, при указании настроек в setting
# class TaskPagination(PageNumberPagination):
#     page_size = 7
#     page_size_query_param = 'page_size'
#     # Максимум 100 объектов на страницу, даже если пользователь просит больше
#     max_page_size = 100


#generics

@extend_schema(tags=['Task'])
class TasksListAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    filterset_class = TaskQueryFilterSerializer


    # функция для фильтрации и ограничения пользователя,
    # чтобы он видел только свои задачи, а админ все
    def get_queryset(self):
        qs = Tasks.objects.task_optimization()
        user = self.request.user

        if user.is_staff:
            return qs

        return qs.filter(assignee=user)

    # queryset = Tasks.objects.task_optimization()

    # queryset = (Tasks.objects
    #              .select_related("assignee", "project")
    #              .prefetch_related("tags", "comments")
    #              .all().order_by( '-id'))


    # permission_classes = [IsAdminUser]

    # Добавляю пагинацию во вьюшку
    # pagination_class = TaskPagination

    # Добавляю кастомный пагинатор
    # pagination_class = CustomPagination

    # Фильтрация
    # filterset_class = TaskQueryFilterSerializer


    @extend_schema(
        summary="Get all tasks",
        description="Get all tasks",

        request=TaskQueryFilterSerializer,
        responses={200: TaskSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    @extend_schema(
        summary="Create task",
        description="Create task",
        request=TaskSerializer,
        responses={201: TaskSerializer},
    )
    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)


@extend_schema(tags=['Task'])
class TaskDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Tasks.objects.task_optimization()
    serializer_class = TaskSerializer


    @extend_schema(
        summary="Get task by id",
        description="Get task by id",
        responses={200: TaskSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update task by id",
        description="Update task by id",
        request=TaskSerializer,
        responses={200: TaskSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete task by id",
        description="Delete task by id",)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# используя классы вместо функций

# class TasksListAPIView(APIView):
#     """
#     List all tasks, or create a new task.
#     """
#
#     def get(self, request, format=None):
#         tasks = (Tasks.objects
#                  .select_related("assignee", "project")
#                  .prefetch_related("tags", "comments")
#                  .all().order_by( '-id'))
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class TaskDetailAPIView(APIView):
#     """
#     Retrieve, update or delete a tasks instance.
#     """
#
#     def get_object(self, pk):
#         try:
#             return Tasks.objects.get(pk=pk)
#         except Tasks.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         task = Tasks.objects.get(pk=pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# используя rest_framework.response через @api_view (+markdown)

# @api_view(["GET", "POST"])
# def tasks_list(request):
#     """
#     List all code tasks, or create a new task.
#     """
#     if request.method == "GET":
#         tasks = (Tasks.objects
#                  .select_related("assignee", "project")
#                  .prefetch_related("tags", "comments")
#                  .all().order_by( '-id'))
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#
#     elif request.method == "POST":
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def task_detail(request, pk):
#     """
#     Retrieve, update or delete a code task.
#     """
#     try:
#         task = Tasks.objects.get(pk=pk)
#     except Tasks.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# используя JsonResponse

# @csrf_exempt
# def tasks_list(request):
#     """
#     List all code tasks, or create a new task.
#     """
#     if request.method == "GET":
#         tasks = (Tasks.objects
#                  .select_related("assignee", "project")
#                  .prefetch_related("tags", "comments")
#                  .all().order_by( '-id'))
#         serializer = TaskSerializer(tasks, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def task_detail(request, pk):
#     """
#     Retrieve, update or delete a code task.
#     """
#     try:
#         task = Tasks.objects.get(pk=pk)
#     except Tasks.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == "GET":
#         serializer = TaskSerializer(task)
#         return JsonResponse(serializer.data)
#
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = TaskSerializer(task, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#         task.delete()
#         return HttpResponse(status=204)