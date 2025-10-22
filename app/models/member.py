from datetime import datetime

from pydantic import BaseModel, EmailStr


class MemberBase(BaseModel):
    name: str
    email: EmailStr


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class Member(MemberBase):
    id: int
    joined_at: datetime
