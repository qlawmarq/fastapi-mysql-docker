from pydantic import BaseModel, EmailStr


class SignInRequestModel(BaseModel):
    email: str
    password: str


class SignUpRequestModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserUpdateRequestModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


class UserAuthResponseModel(BaseModel):
    token: TokenModel
    user: UserResponseModel
