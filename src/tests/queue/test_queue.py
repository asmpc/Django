import random
import unittest

from task_manager.queue import UniqueQueue, EmptyUniqueQueueError



# Unique Queue FIFO
class TestUniqueQueueFifo(unittest.TestCase):

    def setUp(self):
        strategy = "FIFO"
        self.queue = UniqueQueue(strategy)

    def test_queue_exist(self):
        queue = UniqueQueue()

    def test_queue_exist_strategy(self):
        queue = UniqueQueue("FIFO")

    def test_no_exist_strategy(self):
        with self.assertRaises(TypeError):
            self.queue = UniqueQueue("FIFA")

    def test_add_unique_item_to_unique_queue(self):
        # queue = UniqueQueue("FIFO")
        item_1 = 5
        item_2 = 5
        len_unique_queue = 1
        self.queue.add(item_1)
        self.queue.add(item_2)
        item = self.queue.storage[0]
        self.assertEqual(item_1, item)
        self.assertEqual(item_2, item)
        self.assertEqual(len_unique_queue, len(self.queue.storage) == 1)

    def test_add_and_get_item_from_unique_queue(self):
        item_1 = 5
        self.queue.add(item_1)
        item = self.queue.remove()
        self.assertEqual(item_1, item)

    def test_get_item_from_empty_unique_queue(self):
        with self.assertRaises(EmptyUniqueQueueError):
            self.queue.remove()

    def test_add_and_get_multi_value_from_unique_queue(self):
        item_1 = 5
        item_2 = 6
        item_3 = 7
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        item = self.queue.remove()
        self.assertEqual(item_1, item)
        item = self.queue.remove()
        self.assertEqual(item_2, item)
        item = self.queue.remove()
        self.assertEqual(item_3, item)

    def test_add_random_items_to_unique_queue(self):
        item_1 = 5
        self.queue.add(item_1)
        for i in range(10):
            self.queue.add(random.randint(1, 10))
        item = self.queue.remove()
        self.assertEqual(item_1, item)

    def test_len_of_unique_queue(self):
        item_1 = 5
        item_2 = 6
        item_3 = 7
        len_unique_queue = 3
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        self.assertEqual(len_unique_queue, len(self.queue.storage))

    def test_last_item_from_unique_queue(self):
        item_1 = 5
        item_2 = 6
        item_3 = 7
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        item = self.queue.storage[-1]
        self.assertEqual(item_3, item)



#Unique Queue LIFO
class TestUniqueQueueLifo(unittest.TestCase):

    def setUp(self):
        strategy = "LIFO"
        self.queue = UniqueQueue(strategy)

    def test_queue_exist(self):
        queue = UniqueQueue()

    def test_queue_exist_strategy(self):
        queue = UniqueQueue("LIFO")

    def test_no_exist_strategy(self):
        with self.assertRaises(TypeError):
            self.queue = UniqueQueue("LIFA")

    def test_add_unique_item_to_unique_queue(self):
        item_1 = 5
        item_2 = 5
        len_unique_queue = 1
        self.queue.add(item_1)
        self.queue.add(item_2)
        item = self.queue.storage[0]
        self.assertEqual(item_1, item)
        self.assertEqual(item_2, item)
        self.assertEqual(len_unique_queue, len(self.queue.storage) == 1)

    def test_add_and_get_item_from_unique_queue(self):
        item_1 = 5
        self.queue.add(item_1)
        item = self.queue.remove()
        self.assertEqual(item_1, item)

    def test_get_item_from_empty_unique_queue(self):
        with self.assertRaises(EmptyUniqueQueueError):
            self.queue.remove()

    def test_add_and_get_multi_value_from_unique_queue(self):
        item_1 = 5
        item_2 = 6
        item_3 = 7
        self.queue.add(item_1)
        self.queue.add(item_2)
        self.queue.add(item_3)
        item = self.queue.remove()
        self.assertEqual(item_3, item)
        item = self.queue.remove()
        self.assertEqual(item_2, item)
        item = self.queue.remove()
        self.assertEqual(item_1, item)

    def test_add_random_items_to_unique_queue(self):
        item_1 = 5
        self.queue.add(item_1)
        for i in range(10):
            self.queue.add(random.randint(1, 10))
        item = self.queue.remove()
        self.assertNotEqual(item_1, item)

    def test_len_of_unique_queue(self):
        self.queue.add(5)
        self.queue.add(6)
        self.queue.add(7)
        self.assertEqual(3, len(self.queue.storage))

    def test_last_item_from_unique_queue(self):
        self.queue.add(5)
        self.queue.add(6)
        self.queue.add(7)
        item = self.queue.storage[-1]
        self.assertEqual(5, item)



if __name__ == '__main__':
    unittest.main()