from task_manager.models import Comments
from task_manager.v1.serializers import CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets



# используя ViewSet

@extend_schema_view(
    list=extend_schema(summary="Get all comments"),
    retrieve=extend_schema(summary="Get comment by id"),
    create=extend_schema(summary="Create comment"),
    update=extend_schema(summary="Update comment by id"),
    partial_update=extend_schema(summary="Partial update comment by id"),
    destroy=extend_schema(summary="Delete comment by id"),
)
@extend_schema(tags=['Comment'])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = (Comments.objects
                .prefetch_related("user", "task")
                .all().order_by( '-id')
                )
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination


# Пагинация, без привязки к настройкам в setting

# class CommentPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100
#
#
# @extend_schema(tags=['Comment'])
# class CommentsListAPIView(APIView):
#     """
#     List all comments, or create a new comment.
#     """
#
#     def get(self, request, format=None):
#         comments = (Comments.objects
#                        .prefetch_related("user", "task")
#                        .all().order_by( '-id')
#                        )
#
#         paginator = CommentPagination()
#         page = paginator.paginate_queryset(comments, request)
#
#         serializer = CommentSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)
#
#         # До пагинации
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @extend_schema(tags=['Comment'])
# class CommentDetailAPIView(APIView):
#     """
#     Retrieve, update or delete a comment instance.
#     """
#
#     def get_object(self, pk):
#         try:
#             return Comments.objects.get(pk=pk)
#         except Comments.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         comment = Comments.objects.get(pk=pk)
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         comment = self.get_object(pk)
#         serializer = CommentSerializer(comment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         comment = self.get_object(pk)
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)