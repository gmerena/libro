from fastapi import APIRouter

from app.api.routes import books_router, loans_router, members_router

router = APIRouter()

router.include_router(members_router, prefix="/members", tags=["members"])
router.include_router(books_router, prefix="/books", tags=["books"])
router.include_router(loans_router, prefix="/loans", tags=["loans"])


@router.get("/")
async def read_root():
    return {"message": "Libro Könyvtár API", "version": "1.0.0", "endpoints": {"members": "/members", "books": "/books", "loans": "/loans"}}
