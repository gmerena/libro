
from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str


class BookCreate(BookBase):
    available: bool = True


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    available: bool | None = None


class Book(BookBase):
    id: int
    available: bool

    class Config:
        from_attributes = True
