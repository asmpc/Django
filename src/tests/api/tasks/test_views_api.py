from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from account.models import User
from task_manager.models import Tasks

class TestTaskApiView(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
        )
        self.path = "/api/tasks/"

        self.test_task_name_1 = "Task 1"
        self.test_description_1 = "Task 1"
        self.test_priority_1 = 2
        self.test_task_name_2 = "Task 2"
        self.test_description_2 = "Task 2"
        self.test_priority_2 = 4

        self.data_1 = {
            "name": self.test_task_name_1,
            "priority": self.test_priority_1,
            "description": self.test_description_1
        }

        self.data_2 = {
            "name": self.test_task_name_2,
            "priority": self.test_priority_2,
            "description": self.test_description_2
        }


    def test_no_tasks_user_unauthorized(self):

        response = self.client.get(self.path)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_tasks_user_authorized(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.path)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_task_user_authorized(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            path=self.path,
            data=self.data_1
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json()['name'],
            self.test_task_name_1
        )

        self.assertEqual(
            response.json()["description"],
            self.test_description_1
        )
        self.assertEqual(
            response.json()["priority"],
            self.test_priority_1
        )

        tasks = Tasks.objects.all()
        self.assertEqual(len(tasks), 1)

    def test_delete_task_user_authorized(self):

        self.test_task = Tasks.objects.create(
            name=self.test_task_name_1,
            description=self.test_description_1,
            priority=self.test_priority_1
        )

        self.client.force_authenticate(user=self.user)

        self.detail_path = f"/api/tasks/{self.test_task.id}/"

        response = self.client.delete(self.detail_path)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tasks.objects.filter(id=self.test_task.id).exists())

    def test_put_task_user_authorized(self):

        self.test_task = Tasks.objects.create(
            name=self.test_task_name_1,
            description=self.test_description_1,
            priority=self.test_priority_1
        )

        self.client.force_authenticate(user=self.user)

        self.detail_path = f"/api/tasks/{self.test_task.id}/"

        response = self.client.put(
            self.detail_path,
            self.data_2,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json()['name'],
            self.test_task_name_2
        )

        self.assertEqual(
            response.json()["description"],
            self.test_description_2
        )
        self.assertEqual(
            response.json()["priority"],
            self.test_priority_2
        )

        tasks = Tasks.objects.all()
        self.assertEqual(len(tasks), 1)















