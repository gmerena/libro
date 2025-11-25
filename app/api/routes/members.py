from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DatabaseDep

from ...models.common import PaginatedResponse, ResponseModel
from ...models.member import Member, MemberCreate, MemberUpdate

router = APIRouter(prefix="/members", tags=["members"])


@router.get("", response_model=PaginatedResponse[Member])
async def get_members(db: DatabaseDep, take: int = Query(default=10, ge=1, le=1000), skip: int = Query(default=0, ge=0)):

    rows = await db.fetch("SELECT * FROM members OFFSET $1 LIMIT $2", skip, take)

    members = [Member(**row) for row in rows]

    total = await db.fetchval("SELECT COUNT(*) FROM members")
    return PaginatedResponse.create(members, total, skip // take + 1, take)


@router.get("/{member_id}", response_model=Member)
async def get_member(db: DatabaseDep, member_id: int):
    row = await db.fetchrow("SELECT * FROM members WHERE id = $1", member_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag ({member_id}) nem található")
    return Member(**row)


@router.post("", response_model=Member, status_code=status.HTTP_201_CREATED)
async def create_member(db: DatabaseDep, member_in: MemberCreate):
    existing = await db.fetchrow("SELECT * FROM members WHERE email = $1", member_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ez az email cím már használatban van.")

    row = await db.fetchrow(
        """
        INSERT INTO members (name, email, joined_at)
        VALUES ($1, $2, NOW())
        RETURNING *
        """,
        member_in.name,
        member_in.email,
    )

    return Member(**row)


@router.put("/{member_id}", response_model=Member)
async def update_member(db: DatabaseDep, member_id: int, member_in: MemberUpdate):
    existing = await db.fetchrow("SELECT * FROM members WHERE id = $1", member_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag ({member_id}) nem található")

    if member_in.email and member_in.email != existing["email"]:
        email_used = await db.fetchrow("SELECT * FROM members WHERE email = $1 AND id != $2", member_in.email, member_id)
        if email_used:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ez az email cím már használatban van.")

    updated_member = existing.copy()
    if member_in.name is not None:
        updated_member["name"] = member_in.name
    if member_in.email is not None:
        updated_member["email"] = member_in.email

    row = await db.fetchrow(
        """
        UPDATE members
        SET name = $1, email = $2
        WHERE id = $3
        RETURNING *
        """,
        updated_member["name"],
        updated_member["email"],
        member_id,
    )
    return Member(**row)


@router.delete("/{member_id}", response_model=ResponseModel)
async def delete_member(db: DatabaseDep, member_id: int):
    existing = await db.fetchrow("SELECT * FROM members WHERE id = $1", member_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag ({member_id}) nem található")

    active_loan = await db.fetchrow("SELECT 1 FROM loans WHERE member_id = $1 AND return_date IS NULL", member_id)
    if active_loan:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tag ({member_id}) aktív kölcsönzésekkel rendelkezik, ezért nem törölhető.")

    await db.execute("DELETE FROM members WHERE id = $1", member_id)
    return ResponseModel(message="Tag sikeresen törölve.")
