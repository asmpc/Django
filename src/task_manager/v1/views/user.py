from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from account.models import User
from task_manager.v1.serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from drf_spectacular.utils import extend_schema





@extend_schema(tags=['User'])
class UsersListAPIView(APIView):
    """
    List all users, or create a new user.
    """

    @extend_schema(
        summary="Get all users",
        description="Get all users",
        responses={200: UserSerializer},
    )
    def get(self, request, format=None):
        users = User.objects.all().order_by('-id')

        # создаём paginator
        paginator_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = paginator_class()

        # разбиваю queryset
        page = paginator.paginate_queryset(users, request)

        # возвращаю
        serializer = UserSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

        # serializer = UserSerializer(users, many=True)
        # return Response(serializer.data)

    @extend_schema(
        summary="Create user",
        description="Create user",
        request=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['User'])
class UserDetailAPIView(APIView):
    """
    Retrieve, update or delete a user instance.
    """


    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Get user by id",
        description="Get user by id",
        responses={200: UserSerializer},
    )
    def get(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        summary="Update user by id",
        description="Update user by id",
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete user by id",
        description="Delete user by id",
    )
    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# используя rest_framework.response (+markdown)

# @api_view(["GET", "POST"])
# def users_list(request):
#     """
#     List all code tasks, or create a new task.
#     """
#     if request.method == "GET":
#         users = User.objects.all().order_by('-id')
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     elif request.method == "POST":
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET", "PUT", "DELETE"])
# def user_detail(request, pk):
#     """
#     Retrieve, update or delete a code task.
#     """
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# используя JsonResponse

# @csrf_exempt
# def users_list(request):
#     """
#     List all code users, or create a new task.
#     """
#     if request.method == "GET":
#         users = User.objects.all().order_by('-id')
#         serializer = UserSerializer(users, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def user_detail(request, pk):
#     """
#     Retrieve, update or delete a code user.
#     """
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == "GET":
#         serializer = UserSerializer(user)
#         return JsonResponse(serializer.data)
#
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(user, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#         user.delete()
#         return HttpResponse(status=204)