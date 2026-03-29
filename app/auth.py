from flask import abort, request

from app.config import Config


def verify_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        abort(401, description="Missing authorization header")

    parts = auth_header.split()

    if len(parts) != 2 or parts[0] != "Bearer":
        abort(401, description="Invalid authorization format")

    token = parts[1]

    if token != Config.JWT_SECRET_KEY:
        abort(403, description="Invalid token")
