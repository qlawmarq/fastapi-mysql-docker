from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserUpdateRequestModel(BaseModel):
    id: int
    email: EmailStr
    password: Optional[str] = None
    first_name: str
    last_name: str

    @validator("password")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
