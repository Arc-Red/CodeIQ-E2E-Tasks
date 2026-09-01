from datetime import datetime, timezone

from .models import (
    NotificationPreferences,
    NotificationPreferencesUpdate,
    User,
)


USERS = [
    User(
        id=1,
        name="John Doe",
        email="john.doe@example.com",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    ),
    User(
        id=2,
        name="Jane Smith",
        email="jane.smith@example.com",
        created_at=datetime(2026, 1, 15, tzinfo=timezone.utc),
    ),
]


NOTIFICATION_PREFERENCES = {
    1: NotificationPreferences(
        email_notifications=True,
        in_app_notifications=True,
    ),
    2: NotificationPreferences(
        email_notifications=True,
        in_app_notifications=True,
    ),
}


def get_user(user_id: int) -> User | None:
    return next(
        (user for user in USERS if user.id == user_id),
        None,
    )


def get_notification_preferences(
    user_id: int,
) -> NotificationPreferences | None:
    if get_user(user_id) is None:
        return None

    return NOTIFICATION_PREFERENCES.get(
        user_id,
        NotificationPreferences(
            email_notifications=True,
            in_app_notifications=True,
        ),
    )


def update_notification_preferences(
    user_id: int,
    preferences: NotificationPreferencesUpdate,
) -> NotificationPreferences | None:
    if get_user(user_id) is None:
        return None

    updated_preferences = NotificationPreferences(
        email_notifications=preferences.email_notifications,
        in_app_notifications=preferences.in_app_notifications,
    )

    NOTIFICATION_PREFERENCES[user_id] = updated_preferences

    return updated_preferences