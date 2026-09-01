from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, StrictBool


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM

class PaginationMetadata(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class TaskListResponse(BaseModel):
    tasks: list[Task]
    metadata: PaginationMetadata


class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class NotificationPreferences(BaseModel):
    email_notifications: bool
    in_app_notifications: bool


class NotificationPreferencesUpdate(BaseModel):
    email_notifications: StrictBool
    in_app_notifications: StrictBool