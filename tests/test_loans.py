import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_loans_empty(client: AsyncClient):
    response = await client.get("/api/loans")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_get_loans_pagination(client: AsyncClient):
    response = await client.get("/api/loans?take=10&skip=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_active_loans_only(client: AsyncClient):
    response = await client.get("/api/loans?active_only=true")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for loan in data["items"]:
        assert loan["return_date"] is None


@pytest.mark.asyncio
async def test_get_all_loans_including_returned(client: AsyncClient):
    response = await client.get("/api/loans?active_only=false")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_get_nonexistent_loan(client: AsyncClient):
    response = await client.get("/api/loans/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_create_loan_invalid_member(client: AsyncClient):
    loan_data = {"member_id": 99999, "book_id": 99999}
    response = await client.post("/api/loans", json=loan_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_member_active_loans(client: AsyncClient):
    response = await client.get("/api/loans/member/99999/active")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_member_loan_history(client: AsyncClient):
    response = await client.get("/api/loans/member/99999/history")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_book_loan_history(client: AsyncClient):
    response = await client.get("/api/loans/book/99999/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_overdue_loans(client: AsyncClient):
    response = await client.get("/api/loans/overdue/30")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_overdue_loans_invalid_days(client: AsyncClient):
    response = await client.get("/api/loans/overdue/0")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
