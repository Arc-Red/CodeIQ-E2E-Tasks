from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_notification_preferences():
    response = client.get("/users/1/notification-preferences")

    assert response.status_code == 200

    body = response.json()

    assert "email_notifications" in body
    assert "in_app_notifications" in body
    assert isinstance(body["email_notifications"], bool)
    assert isinstance(body["in_app_notifications"], bool)


def test_update_notification_preferences():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": False,
            "in_app_notifications": True,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email_notifications"] is False
    assert body["in_app_notifications"] is True


def test_update_notification_preferences_accepts_boolean_values():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": True,
            "in_app_notifications": False,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email_notifications"] is True
    assert body["in_app_notifications"] is False


def test_updated_preferences_are_persisted():
    client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": False,
            "in_app_notifications": False,
        },
    )

    response = client.get(
        "/users/1/notification-preferences"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email_notifications"] is False
    assert body["in_app_notifications"] is False


def test_rejects_invalid_email_notification_value():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": "yes",
            "in_app_notifications": True,
        },
    )

    assert response.status_code == 422


def test_rejects_string_boolean_email_notification_value():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": "true",
            "in_app_notifications": True,
        },
    )

    assert response.status_code == 422


def test_rejects_integer_email_notification_value():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": 1,
            "in_app_notifications": True,
        },
    )

    assert response.status_code == 422


def test_rejects_invalid_in_app_notification_value():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": True,
            "in_app_notifications": "yes",
        },
    )

    assert response.status_code == 422


def test_rejects_string_boolean_in_app_notification_value():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": True,
            "in_app_notifications": "false",
        },
    )

    assert response.status_code == 422


def test_rejects_integer_in_app_notification_value():
    response = client.put(
        "/users/1/notification-preferences",
        json={
            "email_notifications": True,
            "in_app_notifications": 0,
        },
    )

    assert response.status_code == 422


def test_get_notification_preferences_user_not_found():
    response = client.get(
        "/users/999999/notification-preferences"
    )

    assert response.status_code == 404


def test_update_notification_preferences_user_not_found():
    response = client.put(
        "/users/999999/notification-preferences",
        json={
            "email_notifications": True,
            "in_app_notifications": True,
        },
    )

    assert response.status_code == 404