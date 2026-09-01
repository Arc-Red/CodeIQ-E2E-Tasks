from datetime import datetime, timezone

from .models import User


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


def get_user(user_id: int) -> User | None:
    return next(
        (user for user in USERS if user.id == user_id),
        None,
    )