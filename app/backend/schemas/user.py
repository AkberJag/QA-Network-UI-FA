"""User pydantic schema"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """shared properties"""

    id: int | None = None
    email: EmailStr | None = None


class UserCreate(UserBase):
    """Properties to receive via API on creation"""

    email: EmailStr | None = None
    password: str


class UserUpdate(UserBase):
    """Properties to receive via API on update"""

    password: str


class UserInDBBase(UserBase):
    id: int | None = None


class UserInDB(UserInDBBase):
    """Additional properties stored in DB"""

    hashed_password: str


class UserOut(UserBase):
    """Additional properties to return via API"""
