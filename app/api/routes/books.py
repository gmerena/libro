from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DatabaseDep

from ...models.book import Book, BookCreate, BookUpdate
from ...models.common import PaginatedResponse, ResponseModel

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=PaginatedResponse[Book])
async def get_books(
    db: DatabaseDep,
    take: int = Query(default=10, ge=1, le=1000),
    skip: int = Query(default=0, ge=0),
    available_only: bool = Query(default=False, description="Csak elérhető könyvek"),
):
    if available_only:
        rows = await db.fetch("SELECT * FROM books WHERE available = true ORDER BY title OFFSET $1 LIMIT $2", skip, take)
        total = await db.fetchval("SELECT COUNT(*) FROM books WHERE available = true")
    else:
        rows = await db.fetch("SELECT * FROM books ORDER BY title OFFSET $1 LIMIT $2", skip, take)
        total = await db.fetchval("SELECT COUNT(*) FROM books")

    books = [Book(**row) for row in rows]
    return PaginatedResponse.create(books, total, skip // take + 1, take)


@router.get("/{book_id}", response_model=Book)
async def get_book(db: DatabaseDep, book_id: int):
    row = await db.fetchrow("SELECT * FROM books WHERE id = $1", book_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Könyv ({book_id}) nem található")
    return Book(**row)


@router.get("/isbn/{isbn}", response_model=Book)
async def get_book_by_isbn(db: DatabaseDep, isbn: str):
    row = await db.fetchrow("SELECT * FROM books WHERE isbn = $1", isbn)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Könyv ISBN ({isbn}) nem található")
    return Book(**row)


@router.get("/search/title/{title}", response_model=list[Book])
async def search_books_by_title(db: DatabaseDep, title: str):
    rows = await db.fetch("SELECT * FROM books WHERE title ILIKE $1 ORDER BY title", f"%{title}%")
    return [Book(**row) for row in rows]


@router.get("/search/author/{author}", response_model=list[Book])
async def search_books_by_author(db: DatabaseDep, author: str):
    rows = await db.fetch("SELECT * FROM books WHERE author ILIKE $1 ORDER BY author, title", f"%{author}%")
    return [Book(**row) for row in rows]


@router.post("", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(db: DatabaseDep, book_in: BookCreate):
    existing = await db.fetchrow("SELECT * FROM books WHERE isbn = $1", book_in.isbn)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ez az ISBN már használatban van.")

    row = await db.fetchrow(
        """
        INSERT INTO books (title, author, isbn, available)
        VALUES ($1, $2, $3, $4)
        RETURNING *
        """,
        book_in.title,
        book_in.author,
        book_in.isbn,
        book_in.available,
    )

    return Book(**row)


@router.put("/{book_id}", response_model=Book)
async def update_book(db: DatabaseDep, book_id: int, book_in: BookUpdate):
    existing = await db.fetchrow("SELECT * FROM books WHERE id = $1", book_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Könyv ({book_id}) nem található")

    if book_in.isbn and book_in.isbn != existing["isbn"]:
        isbn_used = await db.fetchrow("SELECT * FROM books WHERE isbn = $1 AND id != $2", book_in.isbn, book_id)
        if isbn_used:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ez az ISBN már használatban van.")

    updated_book = existing.copy()
    if book_in.title is not None:
        updated_book["title"] = book_in.title
    if book_in.author is not None:
        updated_book["author"] = book_in.author
    if book_in.isbn is not None:
        updated_book["isbn"] = book_in.isbn
    if book_in.available is not None:
        updated_book["available"] = book_in.available

    row = await db.fetchrow(
        """
        UPDATE books
        SET title = $1, author = $2, isbn = $3, available = $4
        WHERE id = $5
        RETURNING *
        """,
        updated_book["title"],
        updated_book["author"],
        updated_book["isbn"],
        updated_book["available"],
        book_id,
    )
    return Book(**row)


@router.patch("/{book_id}/availability", response_model=Book)
async def set_book_availability(db: DatabaseDep, book_id: int, available: bool):
    existing = await db.fetchrow("SELECT * FROM books WHERE id = $1", book_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Könyv ({book_id}) nem található")

    row = await db.fetchrow(
        "UPDATE books SET available = $1 WHERE id = $2 RETURNING *",
        available,
        book_id,
    )
    return Book(**row)


@router.delete("/{book_id}", response_model=ResponseModel)
async def delete_book(db: DatabaseDep, book_id: int):
    existing = await db.fetchrow("SELECT * FROM books WHERE id = $1", book_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Könyv ({book_id}) nem található")

    active_loan = await db.fetchrow("SELECT 1 FROM loans WHERE book_id = $1 AND return_date IS NULL", book_id)
    if active_loan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Könyv ({book_id}) aktív kölcsönzéssel rendelkezik, ezért nem törölhető.")

    await db.execute("DELETE FROM books WHERE id = $1", book_id)
    return ResponseModel(message="Könyv sikeresen törölve.")
