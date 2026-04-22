from task_manager.models import Attachments
from task_manager.v1.serializers import AttachmentSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema



@extend_schema(tags=['Attachment'])
class AttachmentsListAPIView(APIView):
    """
    List all attachments, or create a new attachment.
    """


    @extend_schema(
        summary="Get all attachments",
        description="Get all attachments",
        responses={200: AttachmentSerializer},
    )
    def get(self, request, format=None):
        attachments = (Attachments.objects
                       .prefetch_related("task")
                       .all().order_by( '-id')
                       )
        serializer = AttachmentSerializer(attachments, many=True)
        return Response(serializer.data)


    @extend_schema(
        summary="Create attachment",
        description="Create attachment",
        request=AttachmentSerializer,
        responses={201: AttachmentSerializer},
    )
    def post(self, request, format=None):
        serializer = AttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Attachment'])
class AttachmentDetailAPIView(APIView):
    """
    Retrieve, update or delete an attachment instance.
    """


    def get_object(self, pk):
        try:
            return Attachments.objects.get(pk=pk)
        except Attachments.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Get attachment by id",
        description="Get attachment by id",
        responses={200: AttachmentSerializer},
    )
    def get(self, request, pk, format=None):
        attachment = Attachments.objects.get(pk=pk)
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data)

    @extend_schema(
        summary="Update attachment by id",
        description="Update attachment by id",
        request=AttachmentSerializer,
        responses={200: AttachmentSerializer},
    )
    def put(self, request, pk, format=None):
        attachment = self.get_object(pk)
        serializer = AttachmentSerializer(attachment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete attachment by id",
        description="Delete attachment by id",
    )
    def delete(self, request, pk, format=None):
        attachment = self.get_object(pk)
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)