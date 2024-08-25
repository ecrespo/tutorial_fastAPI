from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None




class User(Document):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str
    date_created: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users_database"

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "disabled": False,
                # "hashed_password": "hashedpassword123",
                "date_created": datetime.now(),
            }
        }


class UserInDB(User):
    hashed_password: str

    class Settings:
        name = "UserINDB"

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "disabled": False,
                "hashed_password": "hashedpassword123",
                "date_created": datetime.now(),
            }
        }