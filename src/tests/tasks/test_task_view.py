from django.test import Client, TestCase



class TestTaskView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_task_list(self):
        response = self.client.get('/tasks/')
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)


