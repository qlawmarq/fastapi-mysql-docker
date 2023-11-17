from pydantic import BaseModel, EmailStr


class UserUpdateRequestModel(BaseModel):
    id: int
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
