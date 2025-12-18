import pytest

from app.services.places import PlacesClient


class DummyResponse:
    def __init__(self, json_data: dict, status_code: int = 200) -> None:
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError("error")

    def json(self) -> dict:
        return self._json


class DummyClient:
    def __init__(self, data: dict) -> None:
        self.data = data

    async def get(self, *args, **kwargs):
        return DummyResponse(self.data)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


@pytest.mark.asyncio
async def test_places_client(monkeypatch):
    client = PlacesClient(api_key="demo")
    payload = {"result": {"items": [{"id": "1", "name": "Cafe"}]}}

    async def fake_async_client(*args, **kwargs):
        return DummyClient(payload)

    monkeypatch.setattr("httpx.AsyncClient", fake_async_client)
    results = await client.search("cafe")
    assert results[0]["name"] == "Cafe"
