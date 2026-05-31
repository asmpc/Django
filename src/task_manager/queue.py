class EmptyUniqueQueueError(Exception):
    pass



class UniqueQueue:
    FIFO = "FIFO"
    LIFO = "LIFO"
    STRATEGIES = [FIFO, LIFO]
    def __init__(self, strategy: str = FIFO):
        self.strategy = strategy
        self.storage = []
        if self.strategy not in self.STRATEGIES:
            raise TypeError("Strategy must be FIFO or LIFO")

    def add(self, item):
        if self.strategy == self.FIFO:
            if item not in self.storage:
                self.storage.append(item)
        if self.strategy == self.LIFO:
            if item not in self.storage:
                self.storage.insert(0, item)

    def remove(self):
        if self.strategy in self.STRATEGIES:
            if not self.storage:
                raise EmptyUniqueQueueError
            return self.storage.pop(0)

    def len_queue(self):
        if self.strategy in self.STRATEGIES:
            return len(self.storage)

    def get_last_item(self):
        if self.strategy in self.STRATEGIES:
            return self.storage[-1]




