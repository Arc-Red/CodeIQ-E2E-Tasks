from .models import Task, TaskCreate, TaskStatus


TASKS = [
    Task(id=1, title="Set up project structure", status=TaskStatus.DONE),
    Task(id=2, title="Implement task listing API", status=TaskStatus.IN_PROGRESS),
    Task(id=3, title="Add status filtering", status=TaskStatus.TODO),
    Task(id=4, title="Add pagination support", status=TaskStatus.TODO),
    Task(id=5, title="Write API tests", status=TaskStatus.IN_PROGRESS),
    Task(id=6, title="Document task API", status=TaskStatus.DONE),
    Task(id=7, title="Add request validation", status=TaskStatus.TODO),
    Task(id=8, title="Review API responses", status=TaskStatus.DONE),
    Task(id=9, title="Add integration tests", status=TaskStatus.TODO),
    Task(id=10, title="Prepare release notes", status=TaskStatus.DONE),
    Task(id=11, title="Improve error handling", status=TaskStatus.IN_PROGRESS),
    Task(id=12, title="Verify pagination metadata", status=TaskStatus.TODO),
    Task(id=13, title="Review task statuses", status=TaskStatus.IN_PROGRESS),
    Task(id=14, title="Clean up API code", status=TaskStatus.DONE),
    Task(id=15, title="Run final test suite", status=TaskStatus.TODO),
]


def list_tasks(
    status: TaskStatus | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Task], int]:
    matching_tasks = TASKS

    if status is not None:
        matching_tasks = [
            task for task in TASKS
            if task.status == status
        ]

    total = len(matching_tasks)

    start = (page - 1) * page_size
    end = start + page_size

    return matching_tasks[start:end], total


def create_task(task_create: TaskCreate) -> Task:
    new_id = max((task.id for task in TASKS), default=0) + 1

    task = Task(
        id=new_id,
        title=task_create.title,
        description=task_create.description,
        status=task_create.status,
    )

    TASKS.append(task)

    return task