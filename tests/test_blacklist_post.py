import uuid


VALID_PAYLOAD = {
    "email": "test@example.com",
    "app_uuid": str(uuid.uuid4()),
    "blocked_reason": "Spam",
}


class TestPostBlacklist:

    def test_add_email_returns_201(self, client, auth_headers):
        payload = {**VALID_PAYLOAD, "app_uuid": str(uuid.uuid4())}
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 201

    def test_add_email_returns_message(self, client, auth_headers):
        payload = {**VALID_PAYLOAD, "app_uuid": str(uuid.uuid4())}
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        data = response.get_json()
        assert "message" in data
        assert "test@example.com" in data["message"]

    def test_add_email_normalizes_to_lowercase(self, client, auth_headers):
        payload = {
            "email": "UPPER@EXAMPLE.COM",
            "app_uuid": str(uuid.uuid4()),
        }
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert "upper@example.com" in data["message"]

    def test_add_email_without_blocked_reason_returns_201(self, client, auth_headers):
        payload = {
            "email": "noreasontest@example.com",
            "app_uuid": str(uuid.uuid4()),
        }
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 201

    def test_add_email_missing_email_returns_400(self, client, auth_headers):
        payload = {"app_uuid": str(uuid.uuid4())}
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 400

    def test_add_email_missing_app_uuid_returns_400(self, client, auth_headers):
        payload = {"email": "test@example.com"}
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 400

    def test_add_email_invalid_uuid_returns_400(self, client, auth_headers):
        payload = {"email": "test@example.com", "app_uuid": "not-a-uuid"}
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 400

    def test_add_email_blocked_reason_too_long_returns_400(self, client, auth_headers):
        payload = {
            "email": "test@example.com",
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": "x" * 256,
        }
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 400

    def test_add_duplicate_email_same_app_returns_409(self, client, auth_headers):
        app_uuid = str(uuid.uuid4())
        payload = {"email": "dup@example.com", "app_uuid": app_uuid}
        client.post("/blacklists", json=payload, headers=auth_headers)
        response = client.post("/blacklists", json=payload, headers=auth_headers)
        assert response.status_code == 409

    def test_add_same_email_different_app_returns_201(self, client, auth_headers):
        payload_1 = {"email": "shared@example.com", "app_uuid": str(uuid.uuid4())}
        payload_2 = {"email": "shared@example.com", "app_uuid": str(uuid.uuid4())}
        client.post("/blacklists", json=payload_1, headers=auth_headers)
        response = client.post("/blacklists", json=payload_2, headers=auth_headers)
        assert response.status_code == 201

    def test_add_email_without_token_returns_401(self, client):
        response = client.post("/blacklists", json=VALID_PAYLOAD)
        assert response.status_code == 401

    def test_add_email_with_invalid_token_returns_403(self, client):
        headers = {"Authorization": "Bearer wrong-token"}
        response = client.post("/blacklists", json=VALID_PAYLOAD, headers=headers)
        assert response.status_code == 403

    def test_add_email_with_malformed_auth_header_returns_401(self, client):
        headers = {"Authorization": "InvalidFormat"}
        response = client.post("/blacklists", json=VALID_PAYLOAD, headers=headers)
        assert response.status_code == 401
