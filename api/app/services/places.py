from typing import Any, Dict, List

import httpx


class PlacesClient:
    def __init__(self, api_key: str, provider: str = "2gis") -> None:
        self.api_key = api_key
        self.provider = provider

    async def search(self, query: str) -> List[Dict[str, Any]]:
        if self.provider != "2gis":
            raise ValueError("Unsupported provider")
        url = "https://catalog.api.2gis.com/3.0/items"
        params = {"q": query, "key": self.api_key, "page_size": 5}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            return data.get("result", {}).get("items", [])
