from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from app.main import app


async def test_liveness_requires_no_dependencies():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


@pytest.mark.parametrize("failed", [False, True])
async def test_readiness_reports_s3_failure_without_exposing_credentials(failed):
    connection = AsyncMock()
    engine = MagicMock()
    engine.connect.return_value.__aenter__.return_value = connection
    app.state.engine = engine
    app.state.s3 = MagicMock()
    app.state.settings = MagicMock(s3_bucket="test")
    if failed:
        app.state.s3.head_bucket.side_effect = RuntimeError("sensitive-secret")
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/ready")
    assert response.status_code == (503 if failed else 200)
    assert "sensitive-secret" not in response.text
