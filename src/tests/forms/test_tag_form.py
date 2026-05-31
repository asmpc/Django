from django.test import Client, TestCase

from account.models import User
from task_manager.models import Tasks, Tags
from django.contrib.auth.models import Permission



class TestsTagForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@admin.ru",
            password="adminpass",
        )
        self.task = Tasks.objects.create(name="Task 1")
        self.test_name_tag = "Tag 1"
        self.path = "/tasks/tag"
        self.data = {
            "name": self.test_name_tag,
            'tasks': [self.task.id],
        }
        self.client = Client()

    def test_anonymous_user_redirected_from_create_Tag(self):

        response = self.client.post(path=self.path, data=self.data)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Tags.objects.filter(
                name=self.test_name_tag
            ).exists()
        )

        self.assertIn(
            "/login/",
            response.url
        )

    def test_authenticated_user_no_can_create_tag_without_permission(self):

        self.client.force_login(self.user)

        response = self.client.post(
            path=self.path,
            data=self.data
        )

        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_create_tag_with_permission(self):
        self.client.force_login(self.user)

        permission = Permission.objects.get(
            codename="add_tags"
        )

        self.user.user_permissions.add(permission)

        response = self.client.post(
            path=self.path,
            data=self.data,
        )

        self.assertEqual(response.status_code, 302)

        tag = Tags.objects.get(
            name=self.test_name_tag
        )

        self.assertIn(
            tag,
            self.task.tags.all()
        )

        self.assertTrue(
            self.task.tags.filter(id=tag.id).exists()
        )

        self.assertTrue(
            tag.tasks.filter(id=self.task.id).exists()
        )


        self.assertIn(
            "/tasks/",
            response.url
        )
