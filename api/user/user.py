from fastapi import HTTPException
from pydantic import BaseModel
from database.query import query_get, query_put, query_update
from .auth import Auth

auth_handler = Auth()

class UserModel(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class AuthModel(BaseModel):
    email: str
    password: str


def register_user(user_model: UserModel):
    user = query_get("SELECT * FROM user WHERE email = %s",(user_model.email))
    if len(user) != 0:
        print(user)
        return 'Account already exists'
    hashed_password = auth_handler.encode_password(user_model.password)
    user = query_put("""
                INSERT INTO user (
                    first_name,
                    last_name,
                    email,
                    password_hash
                ) VALUES (%s,%s,%s,%s)
                """,
                (
                    user_model.first_name,
                    user_model.last_name,
                    user_model.email,
                    hashed_password
                )
    )
    return user

def signin_user(email, password):
    user = query_get("SELECT * FROM user WHERE email = %s",(email))
    if len(user) == 0:
        print('Invalid email')
        raise HTTPException(status_code=401, detail='Invalid email')
    if (not auth_handler.verify_password(password, user[0]['password_hash'])):
        print('Invalid password')
        raise HTTPException(status_code=401, detail='Invalid password')
    return user[0]

def update_user(user_model: UserModel):
        hashed_password = auth_handler.encode_password(user_model.password)
        query_put("""
            UPDATE user 
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    password_hash = %s 
                WHERE user.email = %s;
            """,
            (
                user_model.first_name,
                user_model.last_name,
                user_model.email,
                hashed_password,
                user_model.email,
            )
        )
        user = query_get("SELECT * FROM user WHERE email = %s",(user_model.email))
        return user[0]