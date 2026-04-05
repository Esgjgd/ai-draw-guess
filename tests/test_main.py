from __future__ import annotations

from unittest import mock

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "AI 你画我猜" in response.text


@pytest.mark.asyncio
async def test_guess_endpoint_success() -> None:
    # Mock the global _ai_client
    from app.main import _ai_client

    original_ai_client = _ai_client

    mock_client = mock.AsyncMock()
    mock_client.guess.return_value = "苹果"

    with mock.patch("app.main._ai_client", mock_client):
        payload = {
            "strokes": [
                {
                    "points": [
                        {"x": 10, "y": 10, "t": 100},
                        {"x": 20, "y": 20, "t": 200},
                    ]
                }
            ],
            "width": 640,
            "height": 400,
        }
        response = client.post("/api/guess", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["guess"] == "苹果"
        assert data["raw_text"] == "苹果"
        mock_client.guess.assert_called_once()

    # Restore original
    from app.main import _ai_client as current_ai_client
    current_ai_client = original_ai_client


def test_guess_endpoint_client_not_initialized() -> None:
    from app.main import _ai_client
    original_ai_client = _ai_client

    with mock.patch("app.main._ai_client", None):
        payload = {
            "strokes": [],
            "width": 640,
            "height": 400,
        }
        response = client.post("/api/guess", json=payload)
        assert response.status_code == 500
        assert "AI client not initialized" in response.json()["detail"]

    from app.main import _ai_client as current_ai_client
    current_ai_client = original_ai_client


@pytest.mark.asyncio
async def test_guess_endpoint_external_error() -> None:
    from app.main import _ai_client
    original_ai_client = _ai_client

    mock_client = mock.AsyncMock()
    mock_client.guess.side_effect = RuntimeError("Some external error")

    with mock.patch("app.main._ai_client", mock_client):
        payload = {
            "strokes": [{"points": [{"x": 10, "y": 10, "t": 100}]}],
            "width": 640,
            "height": 400,
        }
        response = client.post("/api/guess", json=payload)
        assert response.status_code == 502
        assert "Some external error" in response.json()["detail"]

    from app.main import _ai_client as current_ai_client
    current_ai_client = original_ai_client


def test_guess_invalid_payload() -> None:
    # Missing required fields
    payload = {
        "strokes": [],
        # Missing width and height
    }
    response = client.post("/api/guess", json=payload)
    assert response.status_code == 422  # Validation error


def test_cors_headers() -> None:
    response = client.get("/api/health", headers={"Origin": "http://example.com"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
