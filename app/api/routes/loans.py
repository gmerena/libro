from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DatabaseDep

from ...models.common import PaginatedResponse, ResponseModel
from ...models.loan import Loan, LoanCreate, LoanWithDetails

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("", response_model=PaginatedResponse[LoanWithDetails])
async def get_loans(
    db: DatabaseDep,
    take: int = Query(default=10, ge=1, le=1000),
    skip: int = Query(default=0, ge=0),
    active_only: bool = Query(default=True, description="Csak aktív kölcsönzések"),
):
    if active_only:
        query = """
            SELECT 
                l.*,
                m.name as member_name,
                m.email as member_email,
                b.title as book_title,
                b.author as book_author,
                b.isbn as book_isbn
            FROM loans l
            JOIN members m ON l.member_id = m.id
            JOIN books b ON l.book_id = b.id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date DESC
            OFFSET $1 LIMIT $2
        """
        rows = await db.fetch(query, skip, take)
        total = await db.fetchval("SELECT COUNT(*) FROM loans WHERE return_date IS NULL")
    else:
        query = """
            SELECT 
                l.*,
                m.name as member_name,
                m.email as member_email,
                b.title as book_title,
                b.author as book_author,
                b.isbn as book_isbn
            FROM loans l
            JOIN members m ON l.member_id = m.id
            JOIN books b ON l.book_id = b.id
            ORDER BY l.loan_date DESC
            OFFSET $1 LIMIT $2
        """
        rows = await db.fetch(query, skip, take)
        total = await db.fetchval("SELECT COUNT(*) FROM loans")

    loans = [LoanWithDetails(**row) for row in rows]
    return PaginatedResponse.create(loans, total, skip // take + 1, take)


@router.get("/{loan_id}", response_model=Loan)
async def get_loan(db: DatabaseDep, loan_id: int):
    row = await db.fetchrow("SELECT * FROM loans WHERE id = $1", loan_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Kölcsönzés ({loan_id}) nem található")
    return Loan(**row)


@router.get("/member/{member_id}/active", response_model=list[Loan])
async def get_member_active_loans(db: DatabaseDep, member_id: int):
    rows = await db.fetch("SELECT * FROM loans WHERE member_id = $1 AND return_date IS NULL ORDER BY loan_date DESC", member_id)
    return [Loan(**row) for row in rows]


@router.get("/member/{member_id}/history", response_model=PaginatedResponse[Loan])
async def get_member_loan_history(db: DatabaseDep, member_id: int, take: int = Query(default=10, ge=1, le=1000), skip: int = Query(default=0, ge=0)):
    rows = await db.fetch("SELECT * FROM loans WHERE member_id = $1 ORDER BY loan_date DESC OFFSET $2 LIMIT $3", member_id, skip, take)
    total = await db.fetchval("SELECT COUNT(*) FROM loans WHERE member_id = $1", member_id)

    loans = [Loan(**row) for row in rows]
    return PaginatedResponse.create(loans, total, skip // take + 1, take)


@router.get("/book/{book_id}/history", response_model=list[Loan])
async def get_book_loan_history(db: DatabaseDep, book_id: int):
    rows = await db.fetch("SELECT * FROM loans WHERE book_id = $1 ORDER BY loan_date DESC", book_id)
    return [Loan(**row) for row in rows]


@router.get("/book/{book_id}/active", response_model=Loan | None)
async def get_book_active_loan(db: DatabaseDep, book_id: int):
    row = await db.fetchrow("SELECT * FROM loans WHERE book_id = $1 AND return_date IS NULL", book_id)
    return Loan(**row) if row else None


@router.get("/overdue/{days}", response_model=list[LoanWithDetails])
async def get_overdue_loans(db: DatabaseDep, days: int = 30):
    if days < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A napok száma legalább 1 kell legyen")

    query = f"""
        SELECT 
            l.*,
            m.name as member_name,
            m.email as member_email,
            b.title as book_title,
            b.author as book_author,
            b.isbn as book_isbn
        FROM loans l
        JOIN members m ON l.member_id = m.id
        JOIN books b ON l.book_id = b.id
        WHERE l.return_date IS NULL 
        AND l.loan_date < NOW() - INTERVAL '{days} days'
        ORDER BY l.loan_date ASC
    """

    rows = await db.fetch(query)
    return [LoanWithDetails(**row) for row in rows]


@router.post("", response_model=Loan, status_code=status.HTTP_201_CREATED)
async def create_loan(db: DatabaseDep, loan_in: LoanCreate):
    member = await db.fetchrow("SELECT * FROM members WHERE id = $1", loan_in.member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag nem található")

    book = await db.fetchrow("SELECT * FROM books WHERE id = $1", loan_in.book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Könyv nem található")

    if not book["available"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A könyv jelenleg nem elérhető")

    active_loan = await db.fetchrow("SELECT * FROM loans WHERE book_id = $1 AND return_date IS NULL", loan_in.book_id)
    if active_loan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A könyv már ki van kölcsönözve")

    member_loan = await db.fetchrow("SELECT * FROM loans WHERE member_id = $1 AND book_id = $2 AND return_date IS NULL", loan_in.member_id, loan_in.book_id)
    if member_loan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A tag már kölcsönözte ezt a könyvet")

    async with db.transaction():
        row = await db.fetchrow(
            """
            INSERT INTO loans (member_id, book_id, loan_date)
            VALUES ($1, $2, NOW())
            RETURNING *
            """,
            loan_in.member_id,
            loan_in.book_id,
        )

        await db.execute("UPDATE books SET available = false WHERE id = $1", loan_in.book_id)

    return Loan(**row)


@router.patch("/{loan_id}/return", response_model=ResponseModel[Loan])
async def return_loan(db: DatabaseDep, loan_id: int, return_date: datetime | None = None):
    """Kölcsönzés visszahozása. Ha return_date nincs megadva, az aktuális időpont kerül beállításra."""
    loan = await db.fetchrow("SELECT * FROM loans WHERE id = $1 AND return_date IS NULL", loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aktív kölcsönzés nem található")

    if return_date is None:
        return_date = datetime.now()

    if return_date < loan["loan_date"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A visszahozás dátuma nem lehet korábbi a kölcsönzés dátumánál")

    async with db.transaction():
        updated_loan = await db.fetchrow(
            "UPDATE loans SET return_date = $1 WHERE id = $2 RETURNING *",
            return_date,
            loan_id,
        )

        await db.execute("UPDATE books SET available = true WHERE id = $1", loan["book_id"])

    return ResponseModel(message="Könyv sikeresen visszahozva", data=Loan(**updated_loan))


@router.delete("/{loan_id}", response_model=ResponseModel)
async def delete_loan(db: DatabaseDep, loan_id: int):
    loan = await db.fetchrow("SELECT * FROM loans WHERE id = $1", loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Kölcsönzés ({loan_id}) nem található")

    async with db.transaction():
        if loan["return_date"] is None:
            await db.execute("UPDATE books SET available = true WHERE id = $1", loan["book_id"])

        await db.execute("DELETE FROM loans WHERE id = $1", loan_id)

    return ResponseModel(message="Kölcsönzés sikeresen törölve.")
