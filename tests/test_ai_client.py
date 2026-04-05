from __future__ import annotations

import pytest
from unittest import mock

import httpx

from app.ai_client import BaishanAIClient
from app.config import Settings


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        baishan_api_key="test-key",
        baishan_model="test-model",
        baishan_base_url="https://api.example.com/v1",
    )


@pytest.mark.asyncio
async def test_guess_success(test_settings: Settings) -> None:
    client = BaishanAIClient(test_settings)

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "苹果"
                }
            }
        ]
    }

    with mock.patch.object(client._client, "post") as mock_post:
        mock_post.return_value = mock.Mock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None,
        )

        result = await client.guess("test prompt")
        assert result == "苹果"

        # Check that the request was built correctly
        call_args = mock_post.call_args
        assert call_args[0][0] == "chat/completions"
        assert "Authorization" in call_args[1]["headers"]
        assert call_args[1]["headers"]["Authorization"] == "Bearer test-key"
        assert call_args[1]["json"]["model"] == "test-model"
        assert call_args[1]["json"]["messages"][0]["content"] == "test prompt"

    await client.aclose()


@pytest.mark.asyncio
async def test_guess_empty_choices(test_settings: Settings) -> None:
    client = BaishanAIClient(test_settings)

    mock_response = {"choices": []}

    with mock.patch.object(client._client, "post") as mock_post:
        mock_post.return_value = mock.Mock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None,
        )

        result = await client.guess("test prompt")
        assert result == ""

    await client.aclose()


@pytest.mark.asyncio
async def test_guess_no_message_content(test_settings: Settings) -> None:
    client = BaishanAIClient(test_settings)

    mock_response = {
        "choices": [
            {
                "message": {}
            }
        ]
    }

    with mock.patch.object(client._client, "post") as mock_post:
        mock_post.return_value = mock.Mock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None,
        )

        result = await client.guess("test prompt")
        assert result == ""

    await client.aclose()


@pytest.mark.asyncio
async def test_guess_raises_on_401(test_settings: Settings) -> None:
    client = BaishanAIClient(test_settings)

    with mock.patch.object(client._client, "post") as mock_post:
        response = mock.Mock()
        response.status_code = 401
        response.text = "Unauthorized"
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=mock.Mock(), response=response
        )
        mock_post.return_value = response

        with pytest.raises(RuntimeError, match="Invalid API Key"):
            await client.guess("test prompt")

    await client.aclose()


@pytest.mark.asyncio
async def test_guess_retries_on_503(test_settings: Settings) -> None:
    client = BaishanAIClient(test_settings)

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "猫咪"
                }
            }
        ]
    }

    with mock.patch.object(client._client, "post") as mock_post:
        # First two calls fail with 503, third succeeds
        def side_effect(*args, **kwargs):
            if mock_post.call_count < 3:
                response = mock.Mock()
                response.status_code = 503
                response.text = "Service Unavailable"
                response.raise_for_status.side_effect = httpx.HTTPStatusError(
                    "Unavailable", request=mock.Mock(), response=response
                )
                return response
            response = mock.Mock()
            response.status_code = 200
            response.json = lambda: mock_response
            response.raise_for_status = lambda: None
            return response

        mock_post.side_effect = side_effect

        result = await client.guess("test prompt")
        assert result == "猫咪"
        assert mock_post.call_count == 3

    await client.aclose()
