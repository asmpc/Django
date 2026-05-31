from django.test import TestCase

from task_manager.models import Tasks
from task_manager.unique_queue_manager import UniqueQueueManager


class TestUniqueQueueFifo(TestCase):

    def setUp(self):

        self.queue = UniqueQueueManager("FIFO")

        self.task_1 = Tasks.objects.create(
            name="Task 1"
        )

        self.task_2 = Tasks.objects.create(
            name="Task 2"
        )

        self.task_3 = Tasks.objects.create(
            name="Task 3"
        )

    def test_add_unique_item_to_unique_queue(self):
        self.queue.add(self.task_1)
        self.queue.add(self.task_1)

        self.assertEqual(
            1,
            self.queue.len_queue()
        )

    def test_add_and_get_item_from_unique_queue(self):
        self.queue.add(self.task_1)

        task = self.queue.remove()

        self.assertEqual(
            self.task_1,
            task
        )

    def test_duplicate_task_not_added(self):
        self.queue.add(self.task_1)
        self.queue.add(self.task_1)

        self.assertEqual(
            1,
            self.queue.len_queue()
        )

    def test_add_and_get_multi_value_from_unique_queue(self):
        self.queue.add(self.task_1)
        self.queue.add(self.task_2)
        self.queue.add(self.task_3)

        self.assertEqual(
            self.task_1,
            self.queue.remove()
        )

        self.assertEqual(
            self.task_2,
            self.queue.remove()
        )

        self.assertEqual(
            self.task_3,
            self.queue.remove()
        )



class TestUniqueQueueLifo(TestCase):
    def setUp(self):

        self.queue = UniqueQueueManager("LIFO")

        self.task_1 = Tasks.objects.create(
            name="Task 1"
        )

        self.task_2 = Tasks.objects.create(
            name="Task 2"
        )

        self.task_3 = Tasks.objects.create(
            name="Task 3"
        )

    def test_add_unique_item_to_unique_queue(self):
        self.queue.add(self.task_1)
        self.queue.add(self.task_1)

        self.assertEqual(
            1,
            self.queue.len_queue()
        )

    def test_add_and_get_item_from_unique_queue(self):
        self.queue.add(self.task_1)

        task = self.queue.remove()

        self.assertEqual(
            self.task_1,
            task
        )

    def test_duplicate_task_not_added(self):
        self.queue.add(self.task_1)
        self.queue.add(self.task_1)

        self.assertEqual(
            1,
            self.queue.len_queue()
        )

    def test_add_and_get_multi_value_from_unique_queue(self):
        self.queue.add(self.task_1)
        self.queue.add(self.task_2)
        self.queue.add(self.task_3)

        self.assertEqual(
            self.task_3,
            self.queue.remove()
        )

        self.assertEqual(
            self.task_2,
            self.queue.remove()
        )

        self.assertEqual(
            self.task_1,
            self.queue.remove()
        )
