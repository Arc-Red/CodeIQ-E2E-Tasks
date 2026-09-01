import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import tasks as tasks_module


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_tasks():
    original_tasks = list(tasks_module.TASKS)
    yield
    tasks_module.TASKS[:] = original_tasks


def test_get_tasks_returns_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200

    body = response.json()

    assert "tasks" in body
    assert "metadata" in body
    assert len(body["tasks"]) > 0

    for task in body["tasks"]:
        assert "id" in task
        assert "title" in task
        assert "status" in task


def test_get_tasks_filters_by_status():
    response = client.get("/tasks?status=TODO")

    assert response.status_code == 200

    body = response.json()

    assert len(body["tasks"]) > 0
    assert all(task["status"] == "TODO" for task in body["tasks"])
    assert body["metadata"]["total"] == len(body["tasks"])


def test_get_tasks_supports_pagination():
    response = client.get("/tasks?page=2&page_size=3")

    assert response.status_code == 200

    body = response.json()

    assert len(body["tasks"]) <= 3
    assert body["metadata"]["page"] == 2
    assert body["metadata"]["page_size"] == 3


def test_pagination_metadata_reflects_filtered_results():
    response = client.get("/tasks?status=DONE&page=1&page_size=2")

    assert response.status_code == 200

    body = response.json()

    assert body["metadata"]["page"] == 1
    assert body["metadata"]["page_size"] == 2
    assert body["metadata"]["total"] == 5
    assert body["metadata"]["total_pages"] == 3


def test_rejects_page_less_than_one():
    response = client.get("/tasks?page=0")

    assert response.status_code == 400


def test_rejects_page_size_less_than_one():
    response = client.get("/tasks?page_size=0")

    assert response.status_code == 400


def test_rejects_page_size_greater_than_100():
    response = client.get("/tasks?page_size=101")

    assert response.status_code == 400


def test_rejects_unsupported_status():
    response = client.get("/tasks?status=BLOCKED")

    assert response.status_code == 422


def test_create_task_returns_created_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Implement API integration",
            "description": "Connect the task service to the backend",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Implement API integration"
    assert body["description"] == "Connect the task service to the backend"
    assert "id" in body


def test_create_task_requires_title():
    response = client.post("/tasks", json={"description": "No title provided"})

    assert response.status_code == 422


def test_create_task_description_is_optional():
    response = client.post("/tasks", json={"title": "Task without description"})

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "Task without description"
    assert body["description"] is None


def test_create_task_defaults_to_todo_status():
    response = client.post("/tasks", json={"title": "Task with default status"})

    assert response.status_code == 201

    body = response.json()

    assert body["status"] == "TODO"


def test_create_task_accepts_valid_explicit_status():
    response = client.post(
        "/tasks",
        json={"title": "Task in progress", "status": "IN_PROGRESS"},
    )

    assert response.status_code == 201

    body = response.json()

    assert body["status"] == "IN_PROGRESS"


def test_create_task_rejects_unsupported_status():
    response = client.post(
        "/tasks",
        json={"title": "Task with bad status", "status": "BLOCKED"},
    )

    assert response.status_code == 422


def test_create_task_generates_created_at_on_server():
    response = client.post("/tasks", json={"title": "Task with timestamp"})

    assert response.status_code == 201

    body = response.json()

    assert "created_at" in body
    assert body["created_at"] is not None


def test_create_task_ignores_client_supplied_created_at():
    response = client.post(
        "/tasks",
        json={
            "title": "Task with spoofed timestamp",
            "created_at": "1999-01-01T00:00:00Z",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["created_at"] != "1999-01-01T00:00:00Z"


def test_create_task_appends_to_existing_tasks_and_is_visible_in_listing():
    create_response = client.post("/tasks", json={"title": "Newly appended task"})
    assert create_response.status_code == 201
    new_task_id = create_response.json()["id"]

    list_response = client.get("/tasks?page_size=100")
    assert list_response.status_code == 200

    ids = [task["id"] for task in list_response.json()["tasks"]]
    assert new_task_id in ids

def test_get_user_profile_returns_user():
    response = client.get("/users/1")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == 1
    assert body["name"] == "John Doe"
    assert body["email"] == "john.doe@example.com"
    assert "created_at" in body


def test_get_user_profile_returns_404_for_unknown_user():
    response = client.get("/users/9999")

    assert response.status_code == 404


def test_get_user_profile_does_not_expose_sensitive_information():
    response = client.get("/users/1")

    assert response.status_code == 200

    body = response.json()

    assert "password" not in body
    assert "password_hash" not in body
    assert "authentication_token" not in body
    assert "token" not in body


def test_get_user_profile_rejects_invalid_user_id():
    response = client.get("/users/not-a-number")

    assert response.status_code == 422