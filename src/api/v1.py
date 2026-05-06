from django.urls import path
from task_manager.v1.views.task import TasksListAPIView, TaskDetailAPIView
from task_manager.v1.views.user import UsersListAPIView, UserDetailAPIView
from task_manager.v1.views.tag import tags_list, tag_detail
from task_manager.v1.views.attachment import AttachmentsListAPIView, AttachmentDetailAPIView
from task_manager.v1.views.comment import CommentViewSet
from task_manager.v1.views.project import ProjectsListAPIView, ProjectDetailAPIView
from task_manager.v1.views.project_detail import ProjectDetailsListAPIView, ProjectDetailsDetailAPIView
from rest_framework.routers import DefaultRouter



# роутинг для ViewSet
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')


urlpatterns = [
    path("tasks/", TasksListAPIView.as_view()),
    path("tasks/<int:pk>/", TaskDetailAPIView.as_view()),
    path("users/", UsersListAPIView.as_view()),
    path("users/<int:pk>/", UserDetailAPIView.as_view()),
    path("tags/", tags_list),
    path("tags/<int:pk>/", tag_detail),
    path("attachments/", AttachmentsListAPIView.as_view()),
    path("attachments/<int:pk>/", AttachmentDetailAPIView.as_view()),
    path("projects/", ProjectsListAPIView.as_view()),
    path("projects/<int:pk>/", ProjectDetailAPIView.as_view()),
    path("project_detail/", ProjectDetailsListAPIView.as_view()),
    path("project_detail/<int:pk>/", ProjectDetailsDetailAPIView.as_view()),

]

urlpatterns += router.urls