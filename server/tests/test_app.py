"""Test module for the main application."""
import pytest
from src.app import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_404_error(client):
    """Test handling of 404 errors."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert "error" in response.json


def test_500_error(client):
    """Test handling of 500 errors."""
    @app.route("/error")
    def error():
        raise Exception("Test error")

    response = client.get("/error")
    assert response.status_code == 500
    assert "error" in response.json 