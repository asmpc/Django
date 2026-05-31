# for Celery

import time
import logging
import requests

from celery import shared_task
from django.contrib.auth import get_user_model

from task_manager.models import Comments, Tasks


logger = logging.getLogger("task_manager")

User = get_user_model()


@shared_task
def send_user_comments_email(user_id):
    """
    Фоновая задача:
    имитирует отправку email пользователю о его комментариях.
    """

    user = User.objects.get(pk=user_id)

    time.sleep(5)

    print(
        f"Email sent to {user.email}. "
        f"User comments page was opened."
    )

    return f"Email sent to {user.email}"


@shared_task
def count_user_comments(user_id):
    """
    Фоновая задача:
    считает количество комментариев пользователя.
    """

    comments_count = Comments.objects.filter(
        user_id=user_id
    ).count()

    time.sleep(5)

    print(
        f"User ID={user_id} has {comments_count} comments."
    )

    return comments_count


@shared_task
def send_tasks_email_to_all_users():
    """
    Имитация рассылки всем пользователям списка задач.
    """

    users = User.objects.all()

    for user in users:
        user_tasks = Tasks.objects.filter(assignee=user)

        print(f"Send email to: {user.email}")
        print(f"Tasks count: {user_tasks.count()}")

        time.sleep(1)

    return "Tasks email newsletter completed"


@shared_task
def cleanup_old_completed_tasks():
    """
    Имитация фоновой очистки старых завершённых задач.
    """

    print("Start cleanup old completed tasks")

    time.sleep(5)

    print("Cleanup completed")

    return "Old completed tasks cleanup completed"

@shared_task
def send_hello_email_to_admin():
    """
    Фоновая задача:
    имитирует отправку приветственного email всем администраторам.
    """

    admins = User.objects.filter(
        is_superuser=True,
        email__isnull=False,
    ).exclude(
        email=""
    )

    sent_count = 0

    for admin in admins:
        print(
            f"Send email to {admin.email}: "
            f"Hello. Are you ready for work?"
        )

        sent_count += 1
        time.sleep(3)

    return {
        "status": "completed",
        "sent_count": sent_count,
    }


@shared_task
def check_dummyjson_products_api():
    """
    Celery-задача:
    проверяет доступность внешнего API dummyjson.com/products.

    При успехе возвращает статус и количество товаров.
    При ошибке пишет информацию в лог и имитирует уведомление администратора.
    """

    url = "https://dummyjson.com/products"

    try:
        response = requests.get(
            url,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        products_count = len(data.get("products", []))

        logger.info(
            "DummyJSON API is available. Products count: %s",
            products_count,
        )

        return {
            "status": "success",
            "api": url,
            "products_count": products_count,
        }

    except requests.RequestException as error:
        logger.error(
            "DummyJSON API is unavailable. Error: %s",
            error,
        )

        admins = User.objects.filter(
            is_superuser=True,
            email__isnull=False,
        ).exclude(
            email="",
        )

        for admin in admins:
            print(
                f"Notify admin {admin.email}: "
                f"DummyJSON API is unavailable. Error: {error}"
            )

        return {
            "status": "error",
            "api": url,
            "error": str(error),
        }