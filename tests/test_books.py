import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_books_empty(client: AsyncClient):
    response = await client.get("/api/books")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_get_books_pagination(client: AsyncClient):
    response = await client.get("/api/books?take=10&skip=0")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


@pytest.mark.asyncio
async def test_get_books_available_only(client: AsyncClient):
    response = await client.get("/api/books?available_only=true")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for book in data["items"]:
        assert book["available"] is True


@pytest.mark.asyncio
async def test_create_book_invalid_isbn(client: AsyncClient):
    book_data = {"title": "Test Book", "author": "Test Author", "isbn": "", "available": True}
    response = await client.post("/api/books", json=book_data)
    assert response.status_code in [400, 422]


@pytest.mark.asyncio
async def test_get_nonexistent_book(client: AsyncClient):
    response = await client.get("/api/books/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_search_books_by_title(client: AsyncClient):
    response = await client.get("/api/books/search/title/test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_search_books_by_author(client: AsyncClient):
    response = await client.get("/api/books/search/author/test")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
