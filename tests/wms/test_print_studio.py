from fastapi.testclient import TestClient

from wms.main import app

client = TestClient(app)


def test_print_studio_endpoint():
    """Test the print studio endpoint successfully loads."""
    response = client.get("/print-studio/")
    assert response.status_code == 200
    assert "Print Studio" in response.text
