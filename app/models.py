from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO


class PaginationMetadata(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class TaskListResponse(BaseModel):
    tasks: list[Task]
    metadata: PaginationMetadata