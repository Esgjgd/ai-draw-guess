from __future__ import annotations

import os
from unittest import mock

import pytest

from app.config import Settings, get_settings


def test_get_settings_valid(monkeypatch) -> None:
    monkeypatch.setenv("BAISHAN_API_KEY", "test-key-123")
    monkeypatch.delenv("BAISHAN_MODEL", raising=False)
    monkeypatch.delenv("BAISHAN_BASE_URL", raising=False)

    settings = get_settings()
    assert isinstance(settings, Settings)
    assert settings.baishan_api_key == "test-key-123"
    assert settings.baishan_model == "DeepSeek-R1-0528"
    assert settings.baishan_base_url == "https://api.edgefn.net/v1"


def test_get_settings_custom_values(monkeypatch) -> None:
    monkeypatch.setenv("BAISHAN_API_KEY", "test-key-123")
    monkeypatch.setenv("BAISHAN_MODEL", "custom-model")
    monkeypatch.setenv("BAISHAN_BASE_URL", "https://custom.api/v1/")

    settings = get_settings()
    assert settings.baishan_api_key == "test-key-123"
    assert settings.baishan_model == "custom-model"
    # Trailing slash should be stripped
    assert settings.baishan_base_url == "https://custom.api/v1"


def test_get_settings_missing_api_key(monkeypatch) -> None:
    monkeypatch.delenv("BAISHAN_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="BAISHAN_API_KEY.*required"):
        get_settings()


def test_get_settings_empty_api_key(monkeypatch) -> None:
    monkeypatch.setenv("BAISHAN_API_KEY", "   ")

    with pytest.raises(RuntimeError, match="BAISHAN_API_KEY.*required"):
        get_settings()
