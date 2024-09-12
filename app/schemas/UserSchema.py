from datetime import datetime
from typing import Optional

from pydantic import BaseModel,EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str


class UserResponseBase(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: str
    disabled: bool
    date_created: datetime
    updated_at: Optional[datetime]

class UserUpdateRequestBase(BaseModel):
    email: EmailStr
    full_name: str
    disabled: bool = False


class UpdatePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str