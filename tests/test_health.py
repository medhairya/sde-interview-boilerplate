def test_health_endpoint(client):
    """
    Test that the health endpoint is reachable and reports healthy
    status for both the database and the API service.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["api"] == "online"
    assert data["services"]["database"] == "connected"
    assert "environment" in data


def test_404_not_found(client):
    """
    Test that requesting an undefined route triggers the custom
    404 exception handler and returns a structured JSON error.
    """
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    
    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert data["error"]["type"] == "NotFoundError"
    assert "not found" in data["error"]["message"].lower()
