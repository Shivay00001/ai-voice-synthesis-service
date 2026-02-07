import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_list_voices():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/voices")
    assert response.status_code == 200
    assert "voices" in response.json()
