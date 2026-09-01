from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


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