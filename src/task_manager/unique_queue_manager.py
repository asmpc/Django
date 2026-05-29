from task_manager.models import Tasks
from task_manager.models import UniqueQueue


class EmptyUniqueQueueError(Exception):
    pass


class UniqueQueueManager:

    FIFO = "FIFO"
    LIFO = "LIFO"

    STRATEGIES = [FIFO, LIFO]

    def __init__(self, strategy=FIFO):

        if strategy not in self.STRATEGIES:
            raise TypeError(
                "Strategy must be FIFO or LIFO"
            )

        self.strategy = strategy

    def add(self, task: Tasks):

        UniqueQueue.objects.get_or_create(
            task=task,
            strategy=self.strategy,
        )

    def remove(self):

        queryset = UniqueQueue.objects.filter(
            strategy=self.strategy
        )

        if self.strategy == self.FIFO:
            queue_item = queryset.first()
        else:
            queue_item = queryset.last()

        if queue_item is None:
            raise EmptyUniqueQueueError()

        task = queue_item.task

        queue_item.delete()

        return task

    def len_queue(self):

        return UniqueQueue.objects.filter(
            strategy=self.strategy
        ).count()

    def get_last_item(self):

        queue_item = (
            UniqueQueue.objects
            .filter(strategy=self.strategy)
            .last()
        )

        if queue_item is None:
            return None

        return queue_item.task