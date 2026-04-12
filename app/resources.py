from uuid import UUID

from flask import request
from flask_restful import Resource

from app.auth import verify_token
from app.services import add_email_to_blacklist, check_email_blacklist


class BlacklistResource(Resource):

    def post(self):
        verify_token()

        data = request.get_json() or {}

        email = data.get("email")
        app_uuid = data.get("app_uuid")
        blocked_reason = data.get("blocked_reason")

        if not email or not app_uuid:
            return {"message": "email and app_uuid are required"}, 400

        try:
            UUID(str(app_uuid))
        except ValueError:
            return {"message": "app_uuid must be a valid UUID"}, 400

        if blocked_reason and len(blocked_reason) > 255:
            return {"message": "blocked_reason must be 255 characters or less"}, 400

        ip_address = request.remote_addr
        normalized_email = email.strip().lower()

        entry = add_email_to_blacklist(
            normalized_email,
            str(app_uuid),
            blocked_reason,
            ip_address,
        )

        if entry is None:
            return {"message": "Email already blacklisted for this app"}, 409

        return {"message": f"{normalized_email} added to blacklist"}, 201


class BlacklistCheckResource(Resource):

    def get(self, email):
        verify_token()

        is_blacklisted, reason = check_email_blacklist(email)

        return {"is_blacklisted": is_blacklisted, "blocked_reason": reason}, 200
