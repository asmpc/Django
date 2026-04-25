from django.db import models



class TaskQuerySet(models.QuerySet):
    def task_with_attachments(self):
        from task_manager.models import Attachments
        attachments = Attachments.objects.values_list('task', flat=True)

        return self.filter(id__in=attachments)

    def task_with_assignee(self):
        return self.filter(assignee__isnull=False)

    def task_optimization(self):
        return (self.select_related("assignee", "project")
                .prefetch_related("tags", "comments")
                .all().order_by( '-created_at')
                )


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def task_attachments(self):
        return self.get_queryset().task_with_attachments()

    def task_assignee(self):
        return self.get_queryset().task_with_assignee()

    def task_optimization(self):
        return self.get_queryset().task_optimization()


class AttachmentQuerySet(models.QuerySet):

    def attachment_optimization(self):
        return self.select_related('task').all().order_by('id')


class AttachmentManager(models.Manager):
    def get_queryset(self):
        return AttachmentQuerySet(self.model, using=self._db)

    def attachment_optimization(self):
        return self.get_queryset().attachment_optimization()