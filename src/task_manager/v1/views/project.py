from task_manager.models import Projects
from task_manager.v1.serializers import ProjectSerializer
from rest_framework import status, mixins, generics
from drf_spectacular.utils import extend_schema



@extend_schema(tags=['Project'])
class ProjectsListAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = (Projects.objects
                 .select_related("owner")
                 .prefetch_related("tasks")
                 .all().order_by( '-id'))
    serializer_class = ProjectSerializer

    @extend_schema(
        summary="Get all projects",
        description="Get all projects",
        responses={200: ProjectSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create project",
        description="Create project",
        request=ProjectSerializer,
        responses={201: ProjectSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@extend_schema(tags=['Project'])
class ProjectDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = (Projects.objects
                .select_related("owner")
                .prefetch_related("tasks")
                .all().order_by('-id'))
    serializer_class = ProjectSerializer

    @extend_schema(
        summary="Get project by id",
        description="Get project by id",
        responses={200: ProjectSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update project by id",
        description="Update project by id",
        request=ProjectSerializer,
        responses={200: ProjectSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete project by id",
        description="Delete project by id",
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)