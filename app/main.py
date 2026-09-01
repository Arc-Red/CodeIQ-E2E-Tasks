import math

from fastapi import FastAPI, HTTPException, Query, status

from .models import (
    Task,
    TaskCreate,
    TaskListResponse,
    TaskPriority,
    TaskStatus,
    User,
    NotificationPreferences,
    NotificationPreferencesUpdate,
)
from .tasks import create_task, list_tasks
from .users import (
    get_user,
    get_notification_preferences,
    update_notification_preferences,
)
from .validation import validate_pagination


app = FastAPI(
    title="CodeIQ E2E Tasks API",
    version="1.0.0",
)


@app.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    status: TaskStatus | None = Query(
        default=None,
        description="Filter tasks by status",
    ),
    priority: TaskPriority | None = Query(
        default=None,
        description="Filter tasks by priority",
    ),
    page: int = Query(
        default=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=20,
        description="Number of tasks per page",
    ),
) -> TaskListResponse:
    validate_pagination(page, page_size)

    tasks, total = list_tasks(
        status=status,
        priority=priority,
        page=page,
        page_size=page_size,
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return TaskListResponse(
        tasks=tasks,
        metadata={
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        },
    )


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def post_task(task_create: TaskCreate) -> Task:
    return create_task(task_create)


@app.get("/users/{user_id}", response_model=User)
def get_user_profile(user_id: int) -> User:
    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@app.get(
    "/users/{user_id}/notification-preferences",
    response_model=NotificationPreferences,
)
def get_user_notification_preferences(
    user_id: int,
) -> NotificationPreferences:
    preferences = get_notification_preferences(user_id)

    if preferences is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return preferences


@app.put(
    "/users/{user_id}/notification-preferences",
    response_model=NotificationPreferences,
)
def put_user_notification_preferences(
    user_id: int,
    preferences: NotificationPreferencesUpdate,
) -> NotificationPreferences:
    updated_preferences = update_notification_preferences(
        user_id,
        preferences,
    )

    if updated_preferences is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return updated_preferences