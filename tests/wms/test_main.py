"""Tests for main module."""

from fastapi.testclient import TestClient

from wms.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Wildcard Management System" in response.text
