from task_manager.models import Tags
from task_manager.v1.serializers import TagSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings
from drf_spectacular.utils import extend_schema



@extend_schema(
    tags=['Tag'],
    summary="Get all tags or create tag",
    responses={
        200: TagSerializer(many=True),
        201: TagSerializer,
    },
    request=TagSerializer,
)
@api_view(["GET", "POST"])
def tags_list(request):
    """
    List all code tags, or create a new tag.
    """
    if request.method == "GET":
        tags = (Tags.objects
                .prefetch_related("tasks")
                .all().order_by( '-id'))

        # пагинация (если настроено в setting)
        paginator_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = paginator_class()

        page = paginator.paginate_queryset(tags, request)

        serializer = TagSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


        # до пагинации
        # serializer = TagSerializer(tags, many=True)
        # return Response(serializer.data)

    elif request.method == "POST":
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Tag'],
    summary="Get tag by id or update tag by id or delete tag by id",
    responses={
        200: TagSerializer(many=True),
        201: TagSerializer,
    },
    request=TagSerializer,
)
@api_view(["GET", "PUT", "DELETE"])
def tag_detail(request, pk):
    """
    Retrieve, update or delete a code tag.
    """
    try:
        tag = Tags.objects.get(pk=pk)
    except Tags.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)