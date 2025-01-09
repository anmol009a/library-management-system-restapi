from email import header
from urllib import response
import pytest
from library.db import get_db


def test_get_member_route(client, req_headers):
    response = client.get("/api/members/1", headers=req_headers)
    assert response.status_code == 200
    pass


def test_list_members_route(client, req_headers):
    response = client.get("/api/members", headers=req_headers)
    assert response.status_code == 200
    pass


def test_update_member_route(client, data, req_headers):
    response = client.put(
        "/api/members/1", json=data.update_member(), headers=req_headers
    )
    assert response.status_code == 204
    pass


def test_delete_member_route(client, req_headers):
    response = client.delete("/api/members/1", headers=req_headers)
    assert response.status_code == 204
    pass
