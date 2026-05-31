from django.db import models


class QueueStrategy(models.TextChoices):
    FIFO = "FIFO", "FIFO"
    LIFO = "LIFO", "LIFO"


class UniqueQueue(models.Model):
    task = models.ForeignKey(
        "task_manager.Tasks",
        on_delete=models.CASCADE,
        related_name="queue_items",
    )

    strategy = models.CharField(
        max_length=4,
        choices=QueueStrategy.choices,
        default=QueueStrategy.FIFO,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["task", "strategy"],
                name="unique_task_per_strategy",
            )
        ]

    def __str__(self):
        return f"{self.strategy}: task {self.task_id}"