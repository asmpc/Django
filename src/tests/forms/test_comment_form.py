from django.test import Client, TestCase

from account.models import User
from task_manager.models import Tasks, Comments
from django.contrib.auth.models import Permission



class TestsCommentForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@admin.ru",
            password="adminpass",
        )
        self.task = Tasks.objects.create(name="Task 1")
        self.test_message = "test message"
        self.path = "/tasks/comment"
        self.data = {
            'message': self.test_message,
            'user': self.user.id,
            'task': self.task.id,
        }
        self.client = Client()

    def test_anonymous_user_redirected_from_create_Comment(self):
        response = self.client.post(path=self.path, data=self.data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Comments.objects.filter(
                message=self.test_message
            ).exists()
        )

        self.assertIn(
            "/login/",
            response.url
        )

    def test_authenticated_user_no_can_create_comment_without_permission(self):

        self.client.force_login(self.user)

        response = self.client.post(
            path=self.path,
            data=self.data
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            Comments.objects.filter(
                message=self.test_message
            ).exists()
        )

    def test_authenticated_user_can_create_comment_with_permission(self):
        self.client.force_login(self.user)

        permission = Permission.objects.get(
            codename="add_comments"
        )

        self.user.user_permissions.add(permission)

        response = self.client.post(
            path=self.path,
            data=self.data,
        )

        self.assertEqual(response.status_code, 302)

        comment = Comments.objects.get(
            message=self.test_message
        )

        self.assertEqual(
            comment.task,
            self.task
        )

        self.assertEqual(
            comment.user,
            self.user
        )

        self.assertIn(
            "/tasks/",
            response.url
        )