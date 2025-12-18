import pytest
from httpx import AsyncClient

from app.main import create_app
from app.config import Settings


class DummySettings(Settings):
    places_api_key: str = "demo"


@pytest.mark.asyncio
async def test_health():
    settings = DummySettings(places_provider="2gis", allowed_origins=["*"])  # type: ignore[arg-type]
    app = create_app(settings)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
