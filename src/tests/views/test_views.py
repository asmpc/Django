from django.test import TestCase, Client
from django.contrib.auth.models import Permission

from account.models import User
from task_manager.models import Tasks, Attachments, Comments
from django.urls import reverse
from django.core.cache import cache


class TestsViews(TestCase):

    def setUp(self):
        cache.clear()
        self.client = Client()

        self.user = User.objects.create_user(
            email="admin@admin.ru",
            password="adminpass",
        )

        self.user.is_staff = True
        self.user.save()

        self.task = Tasks.objects.create(
            name="Task 1",
        )

        self.comment = Comments.objects.create(
            task=self.task,
            message="Test comment",
            user=self.user,
        )

        self.attachment = Attachments.objects.create(
            task=self.task,
        )

    def add_permission(self, codename):
        permission = Permission.objects.get(
            codename=codename
        )
        self.user.user_permissions.add(permission)

    def test_home_page_returns_correct_template(self):
        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "home.html"
        )

    def test_tasks_page_no_returns_tasks_without_permission(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("task")
        )

        self.assertEqual(response.status_code, 403)

    def test_tasks_page_returns_tasks_with_permission(self):
        self.client.force_login(self.user)

        self.add_permission("view_tasks")

        response = self.client.get(
            reverse("task")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "tasks.html"
        )

        self.assertIn(
            self.task,
            response.context["tasks"]
        )

    def test_users_page_returns_users_without_permission(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("user")
        )

        self.assertEqual(response.status_code, 403)


    def test_users_page_returns_users_with_permission(self):
        self.client.force_login(self.user)

        self.add_permission("view_user")

        response = self.client.get(
            reverse("user")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "users.html"
        )

        self.assertIn(
            self.user,
            response.context["users"]
        )

    def test_attachments_page_returns_attachments(self):
        self.client.force_login(self.user)

        self.add_permission("view_attachments")

        response = self.client.get(
            reverse("attachments")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "attachments.html"
        )

    def test_urequest_page_returns_user(self):
        self.client.force_login(self.user)

        self.add_permission("view_user")

        response = self.client.get(
            reverse(
                "urequest",
                kwargs={"pk": self.user.pk}
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "urequest.html"
        )

        self.assertEqual(
            response.context["user"],
            self.user
        )