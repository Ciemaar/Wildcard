# ruff: noqa
from fastapi.testclient import TestClient

from wms.main import app

client = TestClient(app)


def test_dashboard_endpoint():
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert "Idea Dashboard" in response.text


# noqa
