import re
import pytest
from library.db import get_db


user = {"name": "Test User", "email": "test@example.com"}


def test_register(auth, app):
    response = auth.register(**user)
    assert response.status_code == 201

    with app.app_context():
        assert (
            get_db()
            .execute("SELECT * FROM members WHERE name = ?", (user.get("name"),))
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("name", "email", "message", "status_code"),
    (
        ("", "test@example.com", "Name is required.", 400),
        ("a", "", "Email is required.", 400),
        ("Test", "john@example.com", "User is already registered.", 409),
    ),
)
def test_register_validate_input(auth, name, email, message, status_code):
    user = {"name": name, "email": email}
    response = auth.register(**user)
    assert status_code == response.status_code
    assert message in response.json["message"]


def test_login(auth):
    auth.register()
    response = auth.login()
    assert response.status_code == 201
    assert response.json["token"] is not None


@pytest.mark.parametrize(
    ("email", "message"),
    (
        ("", "Email is required"),
        ("a", "Invalid Credentials"),
    ),
)
def test_login_validate_input(auth, email, message):
    response = auth.login(email)
    assert message in response.json["message"]


def test_logout(client, auth):
    pass
