import os
from pyclbr import Class
import tempfile

import pytest
from library import create_app
from library.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    auth_route = "/api/auth"

    def __init__(self, client):
        self._client = client

    def register(self, name="test", email="test"):
        return self._client.post(
            f"{self.auth_route}/register", json={"email": email, "name": name}
        )

    def login(self, email="test"):
        return self._client.post(f"{self.auth_route}/login", json={"email": email})

    def logout(self):
        pass
        return self._client.get(f"{self.auth_route}/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


class Data:

    def member(name="test", email="test"):
        return {"name": name, "email": email}

    def update_member(name="updated test", email="testemail2"):
        return {"name": name, "email": email}

    def book(title="Test Book", author="Test Author", year=2021):
        return {"title": title, "author": author, "year": year}

    def update_book(title="Updated Test Book", author="Updated Test Author", year=2022):
        return {"title": title, "author": author, "year": year}


@pytest.fixture
def data():
    return Data


@pytest.fixture
def req_headers(auth):
    auth.register()
    token = auth.login().get_json()["token"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    return headers
