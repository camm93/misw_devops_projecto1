from flask import request
from flask_restful import Resource

from app.auth import verify_token
from app.services import add_email_to_blacklist, check_email_blacklist


class BlacklistResource(Resource):

    def post(self):

        verify_token()

        data = request.get_json()

        email = data.get("email")
        app_uuid = data.get("app_uuid")
        blocked_reason = data.get("blocked_reason")

        ip_address = request.remote_addr

        entry = add_email_to_blacklist(email, app_uuid, blocked_reason, ip_address)

        if entry is None:
            return {"message": "Email already blacklisted for this app"}, 409
        return {"message": f"{email} added to blacklist"}, 201


class BlacklistCheckResource(Resource):

    def get(self, email):

        verify_token()

        is_blacklisted, reason = check_email_blacklist(email)

        return {"is_blacklisted": is_blacklisted, "blocked_reason": reason}, 200
