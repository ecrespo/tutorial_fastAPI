from datetime import datetime

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    full_name: str
    password: str


class UserResponseBase(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    disabled: bool
    date_created: datetime