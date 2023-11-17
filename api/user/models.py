from pydantic import BaseModel, EmailStr
from typing import Optional


class UserUpdateRequestModel(BaseModel):
    id: int
    email: EmailStr
    password: Optional[str] = None
    first_name: str
    last_name: str


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
