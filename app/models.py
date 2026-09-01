from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus


class PaginationMetadata(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class TaskListResponse(BaseModel):
    tasks: list[Task]
    metadata: PaginationMetadata