import datetime
from email import message
import jwt
from functools import wraps

from flask import (
    Blueprint,
    g,
    redirect,
    request,
    session,
    url_for,
    jsonify,
    current_app,
)
from library.db import get_db

# create blueprint for routes
bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# TODO:
# 1. store issued tokens in db/session. why?
# 2. logout. how?
# 3. error handling
# 4. token expiration
# 5. token revocation. how?


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.authorization and request.authorization.token
        if not auth_token:
            return jsonify({"error": "token is missing"}), 403

        try:
            payload = jwt.decode(
                auth_token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired. Please log in again."}
        except jwt.InvalidTokenError:
            return {"message": "Invalid token. Please log in again."}
        else:
            if not payload.get("member_id"):
                return jsonify({"error": "token has no member_id"}), 403

            db = get_db()
            member = db.execute(
                "SELECT * FROM members WHERE member_id = ?", (payload.get("member_id"),)
            ).fetchone()
            if not member:
                return jsonify({"error": "No such member."}), 403

        return f(*args, **kwargs)

    return decorated


# TODO: validate requests
def validate_req(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.get_json():
            return jsonify({"error": "Invalid Request."}), 400
        return f(*args, **kwargs)

    return decorated


@bp.route("/register", methods=("POST",))
def register():
    auth = request.get_json()

    if not auth:
        return {"message": "Invalid Request."}, 400
    elif not auth.get("email"):
        return {"message": "Email is required."}, 400
    elif not auth.get("name"):
        return {"message": "Name is required."}, 400

    # connect to db
    db = get_db()
    try:
        result = db.execute(
            "INSERT INTO members (name, email) VALUES (?, ?)",
            (auth.get("name"), auth.get("email")),
        )
        inserted_id = result.lastrowid
        db.commit()
    except db.IntegrityError:
        return ({"message": "User is already registered."}, 409)

    else:
        return {}, 201


@bp.post("/login")
def login():
    auth = request.get_json()

    if not auth.get("email"):
        return {"message": "Email is required."}, 400

    try:
        # connect to db
        db = get_db()
        # search member
        members = db.execute("SELECT * FROM members WHERE email = ?", (auth["email"],))
        member = members.fetchone()
        if member:
            auth_token = encode_auth_token(member["member_id"])
            return {"token": auth_token}, 201
        else:
            return {"message": "Invalid Credentials."}, 400
    except Exception as e:
        return {"message": str(e)}, 500


@bp.post("/logout")
def logout():
    pass


def encode_auth_token(member_id):
    """
    Generates the Auth Token
    :param member_id: int
    :return string
    """
    payload = {
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=1),
        "member_id": member_id,
    }
    return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")
