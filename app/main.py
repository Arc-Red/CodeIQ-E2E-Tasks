import math

from fastapi import FastAPI, Query, status

from .models import Task, TaskCreate, TaskListResponse, TaskStatus
from .tasks import create_task, list_tasks
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