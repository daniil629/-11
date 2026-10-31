from __future__ import annotations

import json

import pytest
from aiohttp.test_utils import TestClient, TestServer

from app.config import Settings
from app.health import create_health_app


async def test_infrlo_health_endpoints_are_secret_free():
    client = TestClient(TestServer(create_health_app()))
    await client.start_server()
    try:
        for path in ("/", "/health", "/healthz"):
            response = await client.get(path)
            assert response.status == 200
            assert response.headers["Cache-Control"] == "no-store"
            payload = json.loads(await response.text())
            assert payload == {
                "status": "ok",
                "service": "message-keeper",
                "version": "1.2.0",
            }
            assert "token" not in payload
    finally:
        await client.close()


def test_infrlo_port_is_read_from_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("BOT_TOKEN", "123:TEST")
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("PORT", "8080")
    settings = Settings.from_env()
    assert settings.health_port == 8080


def test_infrlo_rejects_invalid_port(monkeypatch, tmp_path):
    monkeypatch.setenv("BOT_TOKEN", "123:TEST")
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    monkeypatch.setenv("PORT", "70000")
    with pytest.raises(RuntimeError, match="PORT"):
        Settings.from_env()
