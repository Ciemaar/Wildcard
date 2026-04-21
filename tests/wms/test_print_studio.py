# ruff: noqa
from fastapi.testclient import TestClient

from wms.main import app

client = TestClient(app)


def test_print_studio_endpoint():
    response = client.get("/print-studio/")
    assert response.status_code == 200
    assert "Print Studio" in response.text


# noqa
