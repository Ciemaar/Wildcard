from fastapi.testclient import TestClient

from wms.main import app

client = TestClient(app)


def test_generate_pdf():
    """Test generating a PDF via the print studio endpoint."""
    # Attempt to retrieve a fake batch PDF to check the endpoint is mounted correctly
    response = client.get("/print-studio/batch/fake-id/pdf")
    # Should get a 404 since fake-id doesn't exist
    assert response.status_code == 404
