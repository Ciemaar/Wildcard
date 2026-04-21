# ruff: noqa
"""Integration tests for required features."""

import httpx
import pytest
from httpx import AsyncClient
from wms.main import app
import re


@pytest.mark.asyncio
async def test_crud_idea_dashboard():
    """Test full CRUD functionality on the Idea Dashboard."""
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Create
        response = await client.post(
            "/dashboard/prompt",
            data={
                "text": "A new test prompt",
                "category": "TestCat",
                "difficulty": "1",
            },
            headers={"HX-Request": "true"},
        )
        assert response.status_code == 200
        assert "A new test prompt" in response.text

        # Read/List (Dashboard)
        response = await client.get("/dashboard/")
        assert response.status_code == 200
        assert "A new test prompt" in response.text

        # Extract prompt ID
        match = re.search(r"prompt-row-([a-f0-9\-]+)", response.text)
        assert match is not None
        prompt_id = match.group(1)

        # Update inline (Status to APPROVED)
        response = await client.patch(
            f"/dashboard/prompt/{prompt_id}/status", data={"status": "APPROVED"}
        )
        assert response.status_code == 200
        assert "APPROVED" in response.text

        # Delete
        response = await client.delete(f"/dashboard/prompt/{prompt_id}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_pdf_generation_layout():
    """Test PDF Generation Logic and ensure a PDF is returned with crop marks instructions via the HTML layout."""
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        # 1. Create a prompt
        response = await client.post(
            "/dashboard/prompt",
            data={"text": "Print Me", "category": "PrintCat", "difficulty": "1"},
        )
        response = await client.get("/dashboard/")

        # Extract prompt ID
        match = re.search(r"prompt-row-([a-f0-9\-]+)", response.text)
        assert match is not None
        prompt_id = match.group(1)

        # Approve it
        await client.patch(
            f"/dashboard/prompt/{prompt_id}/status", data={"status": "APPROVED"}
        )

        # 2. Create batch
        response = await client.post(
            "/print-studio/batch",
            data={"batch_name": "Test Batch", "prompt_ids": [prompt_id]},
        )
        assert response.status_code == 200

        # Extract batch ID
        match = re.search(r"/print-studio/batch/([a-f0-9\-]+)/pdf", response.text)
        assert match is not None
        batch_id = match.group(1)

        # 3. Generate PDF
        response = await client.get(f"/print-studio/batch/{batch_id}/pdf")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

        # The PDF bytes start with %PDF
        assert response.content.startswith(b"%PDF")


@pytest.mark.asyncio
async def test_error_handling():
    """Test edge cases and error handling."""
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Invalid Batch ID
        response = await client.get("/print-studio/batch/fake-id-123/pdf")
        assert response.status_code == 404
        assert "Batch not found" in response.text

        # Missing data on create
        response = await client.post("/dashboard/prompt", data={"text": "Incomplete"})
        assert response.status_code == 422  # Unprocessable Entity (FastAPI validation)

        # Empty batch creation
        response = await client.post(
            "/print-studio/batch", data={"batch_name": "Empty"}
        )
        assert response.status_code == 200
        assert "Error: No prompts selected" in response.text
