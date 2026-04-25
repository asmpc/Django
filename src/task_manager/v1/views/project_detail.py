from task_manager.models import ProjectDetails
from task_manager.v1.serializers import ProjectDetailSerializer
from rest_framework import status, mixins, generics
from drf_spectacular.utils import extend_schema



@extend_schema(tags=['Project_detail'])
class ProjectDetailsListAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = (ProjectDetails.objects
                 .select_related("project")
                 .all().order_by( '-id'))
    serializer_class = ProjectDetailSerializer

    @extend_schema(
        summary="Get all project_details",
        description="Get all project_details",
        responses={200: ProjectDetailSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary="Create project_detail",
        description="Create project_detail",
        request=ProjectDetailSerializer,
        responses={201: ProjectDetailSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@extend_schema(tags=['Project_detail'])
class ProjectDetailsDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = (ProjectDetails.objects
                 .select_related("project")
                 .all().order_by( '-id'))
    serializer_class = ProjectDetailSerializer

    @extend_schema(
        summary="Get project_detail by id",
        description="Get project_detail by id",
        responses={200: ProjectDetailSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update project_detail by id",
        description="Update project_detail by id",
        request=ProjectDetailSerializer,
        responses={200: ProjectDetailSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete project_detail by id",
        description="Delete project_detail by id",
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)