from flask import request, jsonify, make_response, Blueprint
from library.auth import token_required
from library.db import get_db

# create blueprint for routes
bp = Blueprint("books", __name__, url_prefix="/api/books")

# TODO:
# 1. error handling

# Routes for books CRUD
# ---------------------------------------


# Create one
@bp.route("", methods=["POST"])
def create_book():
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    year = data["year"]

    # validate data
    error = None
    if not title:
        error = "title is required."
    elif not author:
        error = "author is required."
    elif not year:
        error = "year is required."

    # create book
    if error is None:
        # connect to db
        db = get_db()
        try:
            result = db.execute(
                "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                (title, author, year),
            )
            inserted_id = result.lastrowid
            db.commit()
        except db.IntegrityError:
            error = f"Book {data['title']} is already registered."
        else:
            return {"book_id": inserted_id, **data}, 201

    return {"error": error}, 400


# Read One
@bp.route("/<int:book_id>", methods=["GET"])
@token_required
def get_book(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE book_id = ?;", (book_id,)).fetchone()
    if not book:
        return {"message": "Book not found"}, 404
    return {**book}, 200


# Read All
@bp.route("", methods=["GET"])
@token_required
def list_books():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 10, type=int)
    offset = (page - 1) * per_page

    db = get_db()
    result = db.execute(
        "SELECT * FROM books LIMIT ? OFFSET ?;", (per_page, offset)
    ).fetchall()
    if not result:
        return {"message": "No books."}, 200

    books = [{**row} for row in result]
    return {
        "books": books,
        "pagination": {
            "page": page,
            "per_page": per_page,
        },
    }


# update one
@bp.route("/<book_id>", methods=["PUT"])
@token_required
def update_book(book_id):
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    year = data["year"]

    # validate data
    error = None
    if not title:
        error = "title is required."
    elif not author:
        error = "author is required."

    if error is None:
        db = get_db()
        db.execute(
            "UPDATE books SET title = ?, author = ?, year = ? WHERE book_id = ?;",
            (title, author, year, book_id),
        )
        db.commit()
        return {}, 204

    return {"error": error}, 400


# delete one
@bp.route("/<int:book_id>", methods=["DELETE"])
@token_required
def delete_book(book_id):
    db = get_db()
    db.execute("DELETE FROM books WHERE book_id = ?;", (book_id,))
    db.commit()
    return {}, 204


# TODO:
# 1. prevent sql injection
# 2. make it parametrized


# search book
@bp.route("/<string:field>/<string:query>", methods=["GET"])
@token_required
def search_books(field, query):
    db = get_db()
    books = db.execute(f"SELECT * FROM `books` WHERE `{field}` LIKE '%{query}%';")
    books = [{**row} for row in books]
    return {"books": books}
