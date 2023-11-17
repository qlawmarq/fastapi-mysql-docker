from datetime import datetime, timedelta
from typing import Annotated
from database import query_get
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os


class TokenData(BaseModel):
    user_email: str | None = None


class AuthUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_email: str


class AuthProvider:
    SECRET_KEY = os.getenv("APP_SECRET_STRING")
    ALGORITHM = "HS256"
    TOKEN_EXPIRE_MINS = 30
    REFRESH_TOKEN_EXPIRE_HOURS = 10
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def __init__(self):
        SECRET_KEY = os.getenv("APP_SECRET_STRING")
        if not SECRET_KEY:
            raise EnvironmentError("APP_SECRET_STRING environment variable not found")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate_user(self, user_email: str, password: str):
        user = self.get_user_by_email(user_email)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def encode_token(self, user_email):
        payload = {
            "exp": datetime.utcnow()
            + timedelta(days=0, minutes=self.TOKEN_EXPIRE_MINS),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": user_email,
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=self.ALGORITHM
            )
            if payload["scope"] == "refresh_token":
                user_email = payload["sub"]
                new_token = self.encode_token(user_email)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    def encode_refresh_token(self, user_email):
        payload = {
            "exp": datetime.utcnow()
            + timedelta(days=0, hours=self.REFRESH_TOKEN_EXPIRE_HOURS),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": user_email,
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user = None
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_email: str = payload.get("sub")
            if user_email is None:
                raise credentials_exception
            token_data = TokenData(user_email=user_email)
        except JWTError:
            raise credentials_exception
        user = self.get_user_by_email(token_data.user_email)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(
        current_user: Annotated[AuthUser, Depends(get_current_user)]
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def get_user_by_email(self, user_email: str):
        user = query_get(
            """
            SELECT
                user.id,
                user.first_name,
                user.last_name,
                user.email,
                user.password_hash
            FROM user
            WHERE email = %s
            """,
            [user_email],
        )
        if len(user) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {user_email} not found",
            )
        return user[0]
