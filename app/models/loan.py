from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, validator


class LoanBase(BaseModel):
    member_id: int
    book_id: int


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    return_date: Optional[datetime] = None


class LoanReturn(BaseModel):
    return_date: datetime = Field(default_factory=datetime.now)


class Loan(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True

    @field_validator("return_date")
    def validate_return_date(cls, v, values):
        """Ellenőrzi, hogy a visszahozás dátuma nem korábbi a kölcsönzés dátumánál"""
        if v is not None and "loan_date" in values and v < values["loan_date"]:
            raise ValueError("A visszahozás dátuma nem lehet korábbi a kölcsönzés dátumánál")
        return v


class LoanWithDetails(Loan):
    member_name: str
    member_email: str
    book_title: str
    book_author: str
    book_isbn: str
