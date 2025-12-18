from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import Settings, get_settings
from .services.places import PlacesClient


class Place(BaseModel):
    id: str
    name: str
    address: str | None = None
    rating: float | None = None
    lat: float | None = None
    lon: float | None = None


class PlacesResponse(BaseModel):
    results: list[Place]


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/places", response_model=PlacesResponse)
    async def places(
        q: str,
        settings_dep: Annotated[Settings, Depends(get_settings)],  # type: ignore
    ) -> PlacesResponse:
        if not q:
            raise HTTPException(status_code=400, detail="Query is required")
        try:
            client = PlacesClient(settings_dep.places_api_key, settings_dep.places_provider)
            raw = await client.search(q)
            results = [
                Place(
                    id=item.get("id") or item.get("data", {}).get("id") or str(idx),
                    name=item.get("name") or item.get("data", {}).get("name", ""),
                    address=item.get("address_name")
                    or (item.get("data", {}).get("address_name"))
                    or "",
                    rating=item.get("rating") or item.get("data", {}).get("rating", {}).get("rating"),
                    lat=item.get("lat") or (item.get("point") or {}).get("lat"),
                    lon=item.get("lon") or (item.get("point") or {}).get("lon"),
                )
                for idx, item in enumerate(raw)
            ]
            return PlacesResponse(results=results)
        except Exception as exc:  # noqa: BLE001
            # keep API responsive, fallback demo result with hint
            return PlacesResponse(
                results=[
                    Place(
                        id="demo",
                        name=q,
                        address="Configure PLACES_API_KEY / provider",
                        rating=None,
                        lat=None,
                        lon=None,
                    )
                ]
            )

    return app


def get_app() -> FastAPI:
    return create_app(get_settings())


app = get_app()
