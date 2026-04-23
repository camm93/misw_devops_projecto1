class TestHealthCheck:

    def test_health_check_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_health_check_returns_expected_body(self, client):
        data = client.get("/").get_json()
        assert data["status"] == "ok"
        assert "version" in data
