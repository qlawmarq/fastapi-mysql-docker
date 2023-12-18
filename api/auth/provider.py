from datetime import datetime, timedelta
from typing import Annotated
from database.connector import DatabaseConnector
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

db_connector = DatabaseConnector()

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)


class TokenData(BaseModel):
    user_email: str | None = None


class AuthUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_email: str


class AuthProvider:
    ALGORITHM = "HS256"
    TOKEN_EXPIRE_MINS = 30
    REFRESH_TOKEN_EXPIRE_HOURS = 10
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self) -> None:
        self.SECRET_KEY = os.getenv("APP_SECRET_STRING")
        if not self.SECRET_KEY:
            raise EnvironmentError("APP_SECRET_STRING environment variable not found")

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return self.PWD_CONTEXT.hash(password)

    def authenticate_user(self, user_email: str, password: str) -> AuthUser:
        user = self.get_user_by_email(user_email)
        if not user:
            raise USER_NOT_FOUND_EXCEPTION
        if not self.verify_password(password, user["password_hash"]):
            raise CREDENTIALS_EXCEPTION
        return user

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.TOKEN_EXPIRE_MINS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def encode_token(self, user_email) -> str:
        payload = {
            "exp": datetime.utcnow()
            + timedelta(days=0, minutes=self.TOKEN_EXPIRE_MINS),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": user_email,
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def refresh_token(self, refresh_token) -> str:
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=self.ALGORITHM
            )
            if payload["scope"] == "refresh_token":
                user_email = payload["sub"]
                new_token = self.encode_token(user_email)
                return new_token
            raise CREDENTIALS_EXCEPTION
        except jwt.ExpiredSignatureError:
            raise CREDENTIALS_EXCEPTION
        except jwt.InvalidTokenError:
            raise CREDENTIALS_EXCEPTION

    def encode_refresh_token(self, user_email) -> str:
        payload = {
            "exp": datetime.utcnow()
            + timedelta(days=0, hours=self.REFRESH_TOKEN_EXPIRE_HOURS),
            "iat": datetime.utcnow(),
            "scope": "refresh_token",
            "sub": user_email,
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def get_current_user(
        self, token: Annotated[str, Depends(OAUTH2_SCHEME)]
    ) -> AuthUser:
        user = None
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_email: str = payload.get("sub")
            if user_email is None:
                raise CREDENTIALS_EXCEPTION
            token_data = TokenData(user_email=user_email)
        except JWTError:
            raise CREDENTIALS_EXCEPTION
        user = self.get_user_by_email(token_data.user_email)
        if user is None:
            raise CREDENTIALS_EXCEPTION
        return user

    def get_user_by_email(self, user_email: str) -> AuthUser:
        user = db_connector.query_get(
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
            raise USER_NOT_FOUND_EXCEPTION
        return user[0]
