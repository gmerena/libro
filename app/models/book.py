from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str


class BookCreate(BookBase):
    available: bool = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    available: Optional[bool] = None


class Book(BookBase):
    id: int
    available: bool

    class Config:
        from_attributes = True
