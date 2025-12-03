import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_members_empty(client: AsyncClient):
    response = await client.get("/api/members")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_get_members_pagination(client: AsyncClient):
    response = await client.get("/api/members?take=5&skip=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


@pytest.mark.asyncio
async def test_create_member_invalid_email(client: AsyncClient):
    member_data = {"name": "Test User", "email": "invalid-email"}
    response = await client.post("/api/members", json=member_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_nonexistent_member(client: AsyncClient):
    response = await client.get("/api/members/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
