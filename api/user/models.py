from pydantic import BaseModel, EmailStr


class UserRequestModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


class UserAuthRequestModel(BaseModel):
    email: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


class UserAuthResponseModel(BaseModel):
    token: TokenModel
    user: UserResponseModel
