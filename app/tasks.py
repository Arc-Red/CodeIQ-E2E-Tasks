from .models import Task, TaskCreate, TaskPriority, TaskStatus


TASKS = [
    Task(
        id=1,
        title="Set up project structure",
        status=TaskStatus.DONE,
        priority=TaskPriority.HIGH,
    ),
    Task(
        id=2,
        title="Implement task listing API",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH,
    ),
    Task(
        id=3,
        title="Add status filtering",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
    ),
    Task(
        id=4,
        title="Add pagination support",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
    ),
    Task(
        id=5,
        title="Write API tests",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH,
    ),
    Task(
        id=6,
        title="Document task API",
        status=TaskStatus.DONE,
        priority=TaskPriority.LOW,
    ),
    Task(
        id=7,
        title="Add request validation",
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
    ),
    Task(
        id=8,
        title="Review API responses",
        status=TaskStatus.DONE,
        priority=TaskPriority.MEDIUM,
    ),
    Task(
        id=9,
        title="Add integration tests",
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
    ),
    Task(
        id=10,
        title="Prepare release notes",
        status=TaskStatus.DONE,
        priority=TaskPriority.LOW,
    ),
    Task(
        id=11,
        title="Improve error handling",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.HIGH,
    ),
    Task(
        id=12,
        title="Verify pagination metadata",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
    ),
    Task(
        id=13,
        title="Review task statuses",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.MEDIUM,
    ),
    Task(
        id=14,
        title="Clean up API code",
        status=TaskStatus.DONE,
        priority=TaskPriority.LOW,
    ),
    Task(
        id=15,
        title="Run final test suite",
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
    ),
]


def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Task], int]:
    matching_tasks = TASKS

    if status is not None:
        matching_tasks = [
            task for task in matching_tasks
            if task.status == status
        ]

    if priority is not None:
        matching_tasks = [
            task for task in matching_tasks
            if task.priority == priority
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
        priority=task_create.priority,
    )

    TASKS.append(task)

    return task