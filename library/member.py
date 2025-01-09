from flask import request, jsonify, make_response, Blueprint
from library import auth
from library.auth import token_required
from library.db import get_db

# create blueprint for routes
bp = Blueprint("members", __name__, url_prefix="/api/members")

# Routes for Members CRUD
# ---------------------------------------


# Create one
# implemented in auth.py


# Read One
@bp.route("/<string:member_id>", methods=["GET"])
@token_required
def get_member(member_id):
    db = get_db()
    member = db.execute(
        "SELECT * FROM members WHERE member_id = ?;", (member_id,)
    ).fetchone()
    if not member:
        return {"message": "Member not found"}, 404
    return {**member}, 200


# Read All
@bp.route("", methods=["GET"])
@token_required
def list_members():
    db = get_db()
    result = db.execute("SELECT * FROM members;").fetchall()
    if not result:
        return {"message": "No Members."}, 200

    members = [{**row} for row in result]
    return {"members": members}


# update one
@bp.route("/<member_id>", methods=["PUT"])
@token_required
def update_member(member_id):
    data = request.get_json()
    name = data["name"]
    email = data["email"]

    # validate data
    error = None
    if not name:
        error = "name is required."
    elif not email:
        error = "email is required."

    if error is None:
        db = get_db()
        db.execute(
            "UPDATE members SET name = ?, email = ? WHERE member_id = ?;",
            (name, email, member_id),
        )
        db.commit()
        return {}, 204

    return {"error": error}, 400


# delete one
@bp.route("/<member_id>", methods=["DELETE"])
@token_required
def delete_member(member_id):
    db = get_db()
    db.execute("DELETE FROM members WHERE member_id = ?;", (member_id,))
    db.commit()
    return {}, 204
