import time
from collections.abc import Callable

from .models import Notification, NotificationStatus


MAX_ATTEMPTS = 3
RETRY_DELAY = 0.1


NOTIFICATIONS = {}


def add_notification(
    notification: Notification,
) -> Notification:
    NOTIFICATIONS[notification.id] = notification
    return notification


def get_notification(
    notification_id: int,
) -> Notification | None:
    return NOTIFICATIONS.get(notification_id)


def deliver_notification(
    notification: Notification,
    delivery_function: Callable[[Notification], None],
) -> Notification:
    for attempt in range(MAX_ATTEMPTS):
        notification.attempts += 1

        try:
            delivery_function(notification)
        except Exception:
            notification.status = NotificationStatus.FAILED

            if notification.attempts < MAX_ATTEMPTS:
                time.sleep(RETRY_DELAY)
                continue

            break

        notification.status = NotificationStatus.DELIVERED
        break

    NOTIFICATIONS[notification.id] = notification

    return notification