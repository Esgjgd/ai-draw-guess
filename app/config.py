from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    baishan_api_key: str
    baishan_model: str
    baishan_base_url: str


def get_settings() -> Settings:
    api_key = os.getenv("BAISHAN_API_KEY", "").strip()
    model = os.getenv("BAISHAN_MODEL", "DeepSeek-R1-0528").strip()
    base_url = os.getenv("BAISHAN_BASE_URL", "https://api.edgefn.net/v1").strip()
    if base_url.endswith("/"):
        base_url = base_url.rstrip("/")

    if not api_key:
        raise RuntimeError("BAISHAN_API_KEY is required")

    return Settings(
        baishan_api_key=api_key,
        baishan_model=model,
        baishan_base_url=base_url,
    )
