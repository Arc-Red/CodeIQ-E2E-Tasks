import pytest

from app.models import Notification, NotificationStatus
from app.notifications import (
    MAX_ATTEMPTS,
    NOTIFICATIONS,
    RETRY_DELAY,
    deliver_notification,
)


@pytest.fixture(autouse=True)
def reset_notifications():
    original_notifications = dict(NOTIFICATIONS)
    NOTIFICATIONS.clear()

    yield

    NOTIFICATIONS.clear()
    NOTIFICATIONS.update(original_notifications)


def test_failed_notification_is_retried(monkeypatch):
    notification = Notification(
        id=1,
        user_id=1,
        message="Test notification",
    )

    attempts = []

    def failing_delivery(notification):
        attempts.append(notification.attempts)
        raise RuntimeError("Delivery failed")

    sleep_calls = []

    monkeypatch.setattr(
        "app.notifications.time.sleep",
        lambda delay: sleep_calls.append(delay),
    )

    result = deliver_notification(
        notification,
        failing_delivery,
    )

    assert result.status == NotificationStatus.FAILED
    assert result.attempts == 3
    assert len(attempts) == 3
    assert sleep_calls == [RETRY_DELAY, RETRY_DELAY]


def test_delivery_stops_after_three_failed_attempts(monkeypatch):
    notification = Notification(
        id=2,
        user_id=1,
        message="Always failing notification",
    )

    delivery_attempts = 0

    def failing_delivery(notification):
        nonlocal delivery_attempts
        delivery_attempts += 1
        raise RuntimeError("Delivery failed")

    monkeypatch.setattr(
        "app.notifications.time.sleep",
        lambda delay: None,
    )

    result = deliver_notification(
        notification,
        failing_delivery,
    )

    assert delivery_attempts == MAX_ATTEMPTS
    assert result.attempts == MAX_ATTEMPTS
    assert result.status == NotificationStatus.FAILED


def test_retry_delay_occurs_between_failed_attempts(monkeypatch):
    notification = Notification(
        id=3,
        user_id=1,
        message="Delayed retry notification",
    )

    sleep_calls = []

    def failing_delivery(notification):
        raise RuntimeError("Delivery failed")

    monkeypatch.setattr(
        "app.notifications.time.sleep",
        lambda delay: sleep_calls.append(delay),
    )

    deliver_notification(
        notification,
        failing_delivery,
    )

    assert len(sleep_calls) == 2
    assert all(delay == RETRY_DELAY for delay in sleep_calls)


def test_notification_tracks_delivery_attempts(monkeypatch):
    notification = Notification(
        id=4,
        user_id=1,
        message="Attempt tracking notification",
    )

    observed_attempts = []

    def failing_delivery(notification):
        observed_attempts.append(notification.attempts)
        raise RuntimeError("Delivery failed")

    monkeypatch.setattr(
        "app.notifications.time.sleep",
        lambda delay: None,
    )

    result = deliver_notification(
        notification,
        failing_delivery,
    )

    assert observed_attempts == [1, 2, 3]
    assert result.attempts == 3


def test_successful_retry_stops_further_attempts(monkeypatch):
    notification = Notification(
        id=5,
        user_id=1,
        message="Eventually successful notification",
    )

    delivery_attempts = 0

    def succeeds_on_second_attempt(notification):
        nonlocal delivery_attempts
        delivery_attempts += 1

        if delivery_attempts == 1:
            raise RuntimeError("Temporary delivery failure")

    sleep_calls = []

    monkeypatch.setattr(
        "app.notifications.time.sleep",
        lambda delay: sleep_calls.append(delay),
    )

    result = deliver_notification(
        notification,
        succeeds_on_second_attempt,
    )

    assert result.status == NotificationStatus.DELIVERED
    assert result.attempts == 2
    assert delivery_attempts == 2
    assert sleep_calls == [RETRY_DELAY]


def test_failed_notification_is_persisted():
    notification = Notification(
        id=6,
        user_id=1,
        message="Persist failed notification",
    )

    def failing_delivery(notification):
        raise RuntimeError("Delivery failed")

    result = deliver_notification(
        notification,
        failing_delivery,
    )

    stored_notification = NOTIFICATIONS[notification.id]

    assert stored_notification.status == NotificationStatus.FAILED
    assert stored_notification.attempts == 3
    assert stored_notification is result    