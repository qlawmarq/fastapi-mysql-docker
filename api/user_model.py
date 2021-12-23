from pydantic import BaseModel

class UserModel(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class AuthModel(BaseModel):
    email: str
    password: str

