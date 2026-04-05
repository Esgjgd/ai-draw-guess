from __future__ import annotations

import logging
from typing import Any

import httpx

from app.config import Settings

logger = logging.getLogger(__name__)


class BaishanAIClient:
    """Client for Baishan AI API with connection reuse and retry logic."""

    MAX_RETRIES = 3
    TIMEOUT = 30.0

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._headers = {
            "Authorization": f"Bearer {settings.baishan_api_key}",
            "Content-Type": "application/json",
        }
        # Create reusable client - connection pooling improves performance
        self._client = httpx.AsyncClient(
            base_url=settings.baishan_base_url,
            timeout=self.TIMEOUT,
            follow_redirects=True,
        )

    async def guess(self, prompt: str) -> str:
        """Send a guess request to Baishan AI with retries for transient errors."""
        payload = {
            "model": self._settings.baishan_model,
            "messages": [{"role": "user", "content": prompt}],
        }

        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(
                    f"Attempting API call to Baishan AI (attempt {attempt + 1}/{self.MAX_RETRIES})"
                )
                logger.debug(f"Using model: {self._settings.baishan_model}")
                logger.debug(f"Prompt length: {len(prompt)} characters")

                response = await self._client.post(
                    "chat/completions", headers=self._headers, json=payload
                )
                response.raise_for_status()
                data: dict[str, Any] = response.json()
                choices = data.get("choices", [])

                if not choices:
                    logger.warning("No choices in API response")
                    return ""

                choice = choices[0]
                message = choice.get("message", {})
                content = message.get("content", "") if isinstance(message, dict) else ""
                result = str(content).strip()
                logger.info(f"API call successful, guess: {result}")
                return result

            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                logger.error(f"API Error: {status} - {exc.response.text}")
                if status in (401, 403):
                    logger.error("API Key appears invalid")
                    raise RuntimeError("Invalid API Key") from exc
                if status == 503 and attempt < self.MAX_RETRIES - 1:
                    logger.info("Retrying due to 503 Service Unavailable")
                    continue
                raise
            except httpx.RequestError as exc:
                logger.error(f"Request error: {exc}")
                if attempt < self.MAX_RETRIES - 1:
                    logger.info("Retrying due to network error")
                    continue
                raise

        # Unreachable code due to retry loop, but needed for type checker
        return ""

    async def aclose(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()