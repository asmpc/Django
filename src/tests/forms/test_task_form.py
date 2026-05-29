from django.test import Client, TestCase

from account.models import User
from task_manager.models import Tasks
from django.contrib.auth.models import Permission



class TestsTasksForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@admin.ru",
            password="adminpass",
        )

        self.client = Client()
        self.test_task_name = "Task 1"
        self.test_description = "Task 1"
        self.test_priority = 2
        self.path = "/tasks/create"

        self.data = {
            "name": self.test_task_name,
            "priority": self.test_priority,
            "description": self.test_description
        }


    def test_anonymous_user_redirected_from_create_task(self):

        response = self.client.post(path=self.path, data=self.data)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Tasks.objects.filter(
                name=self.test_task_name
            ).exists()
        )

        self.assertIn(
            "/login/",
            response.url
        )

    def test_authenticated_user_no_can_create_task_without_permission(self):

        self.client.force_login(self.user)

        response = self.client.post(path=self.path, data=self.data)
        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            Tasks.objects.filter(
                name=self.test_task_name
            ).exists()
        )

    def test_authenticated_user_can_create_task_with_permission(self):

        self.client.force_login(self.user)

        permission = Permission.objects.get(
            codename="add_tasks"
        )

        self.user.user_permissions.add(permission)

        response = self.client.post(path=self.path, data=self.data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Tasks.objects.filter(
                name=self.test_task_name
            ).exists()
        )

        self.assertIn(
            "/tasks/",
            response.url
        )