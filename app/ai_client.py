from __future__ import annotations

import logging
from typing import Any

import httpx

from app.config import Settings

logger = logging.getLogger(__name__)


class BaishanAIClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def guess(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self._settings.baishan_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._settings.baishan_model,
            "messages": [{"role": "user", "content": prompt}],
        }
        
        # Retry logic for transient errors like 503
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting API call to Baishan AI (attempt {attempt + 1}/{max_retries})")
                logger.info(f"Using model: {self._settings.baishan_model}")
                logger.info(f"Prompt length: {len(prompt)}")
                async with httpx.AsyncClient(base_url=self._settings.baishan_base_url, timeout=30) as http_client:
                    response = await http_client.post("chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                data: dict[str, Any] = response.json()
                choices = data.get("choices", [])
                if not choices:
                    logger.warning("No choices in API response")
                    return ""
                choice = choices[0]
                message = choice.get("message", {})
                content = message.get("content", "") if isinstance(message, dict) else ""
                logger.info("API call successful")
                return str(content).strip()
            except httpx.HTTPStatusError as exc:
                logger.error(f"API Error: {exc.response.status_code} - {exc.response.text}")
                if exc.response.status_code in (401, 403):
                    logger.error("API Key appears invalid")
                    raise RuntimeError("Invalid API Key") from exc
                if exc.response.status_code == 503 and attempt < max_retries - 1:
                    logger.info("Retrying due to 503 Service Unavailable")
                    continue  # Retry on 503
                raise
            except httpx.RequestError as exc:
                logger.error(f"Request error: {exc}")
                if attempt < max_retries - 1:
                    logger.info("Retrying due to network error")
                    continue  # Retry on network errors
                raise
        # This line should not be reached, but to satisfy LSP
        return ""