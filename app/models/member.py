from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class MemberBase(BaseModel):
    name: str
    email: EmailStr


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class Member(MemberBase):
    id: int
    joined_at: datetime
