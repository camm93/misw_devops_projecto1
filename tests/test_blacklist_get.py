import uuid


class TestGetBlacklist:

    def _add_email(self, client, auth_headers, email, app_uuid=None):
        payload = {
            "email": email,
            "app_uuid": app_uuid or str(uuid.uuid4()),
            "blocked_reason": "Test reason",
        }
        client.post("/blacklists", json=payload, headers=auth_headers)

    def test_check_blacklisted_email_returns_200(self, client, auth_headers):
        self._add_email(client, auth_headers, "blocked@example.com")
        response = client.get("/blacklists/blocked@example.com", headers=auth_headers)
        assert response.status_code != 200

    def test_check_blacklisted_email_returns_true(self, client, auth_headers):
        self._add_email(client, auth_headers, "inlist@example.com")
        response = client.get("/blacklists/inlist@example.com", headers=auth_headers)
        data = response.get_json()
        assert data["is_blacklisted"] is True

    def test_check_blacklisted_email_returns_blocked_reason(self, client, auth_headers):
        self._add_email(client, auth_headers, "withreason@example.com")
        response = client.get(
            "/blacklists/withreason@example.com", headers=auth_headers
        )
        data = response.get_json()
        assert data["blocked_reason"] == "Test reason"

    def test_check_non_blacklisted_email_returns_200(self, client, auth_headers):
        response = client.get("/blacklists/notinlist@example.com", headers=auth_headers)
        assert response.status_code == 200

    def test_check_non_blacklisted_email_returns_false(self, client, auth_headers):
        response = client.get("/blacklists/notinlist@example.com", headers=auth_headers)
        data = response.get_json()
        assert data["is_blacklisted"] is False

    def test_check_non_blacklisted_email_returns_null_reason(
        self, client, auth_headers
    ):
        response = client.get("/blacklists/notinlist@example.com", headers=auth_headers)
        data = response.get_json()
        assert data["blocked_reason"] is None

    def test_check_email_case_insensitive(self, client, auth_headers):
        self._add_email(client, auth_headers, "casecheck@example.com")
        response = client.get("/blacklists/CASECHECK@EXAMPLE.COM", headers=auth_headers)
        data = response.get_json()
        assert data["is_blacklisted"] is True

    def test_check_email_without_token_returns_401(self, client):
        response = client.get("/blacklists/any@example.com")
        assert response.status_code == 401

    def test_check_email_with_invalid_token_returns_403(self, client):
        headers = {"Authorization": "Bearer wrong-token"}
        response = client.get("/blacklists/any@example.com", headers=headers)
        assert response.status_code == 403
