from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Művelet sikeres"
    data: T | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int = 1
    size: int = 10
    pages: int

    @classmethod
    def create(cls, items: list[T], total: int, page: int = 1, size: int = 10):
        pages = (total + size - 1) // size
        return cls(items=items, total=total, page=page, size=size, pages=pages)


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str | None = None
    details: dict | None = None
