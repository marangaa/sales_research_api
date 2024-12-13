import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_initiate_research(client: TestClient, api_key_headers: Dict[str, str]):
    response = client.post(
        "/api/v1/research",
        headers=api_key_headers,
        json={
            "company_url": "https://example.com",
            "depth": "basic",
            "focus_areas": ["tech_stack"],
            "output_format": "json"
        }
    )

    assert response.status_code == 200
    assert "job_id" in response.json()


def test_get_research_status(client: TestClient, api_key_headers: Dict[str, str]):
    # First create a job
    create_response = client.post(
        "/api/v1/research",
        headers=api_key_headers,
        json={
            "company_url": "https://example.com",
            "depth": "basic",
            "output_format": "json"
        }
    )

    job_id = create_response.json()["job_id"]

    # Then check its status
    status_response = client.get(
        f"/api/v1/research/{job_id}",
        headers=api_key_headers
    )

    assert status_response.status_code == 200
    assert "status" in status_response.json()
    assert "progress" in status_response.json()