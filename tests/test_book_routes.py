import pytest
from library.db import get_db


def test_create_book(client, data, req_headers):
    response = client.post("/api/books", json=data.book(), headers=req_headers)
    assert response.status_code == 201


def test_get_book(client, req_headers):
    response = client.get("/api/books/1", headers=req_headers)
    assert response.status_code == 200
    pass


def test_list_books(client, req_headers):
    response = client.get("/api/books", headers=req_headers)
    assert response.status_code == 200
    pass


def test_update_book(client, data, req_headers):
    response = client.put("/api/books/2", json=data.update_book(), headers=req_headers)
    assert response.status_code == 204
    pass


def test_search_books(client, req_headers):
    response = client.get("/api/books/title/Test Book", headers=req_headers)
    assert response.status_code == 200
    pass


def test_delete_book_route(client, req_headers):
    response = client.delete("/api/books/1", headers=req_headers)
    assert response.status_code == 204
    pass
