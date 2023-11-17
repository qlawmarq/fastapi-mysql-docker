from fastapi import HTTPException, status
from database.query import query_put
from auth.provider import AuthProvider
from auth.models import SignUpRequestModel
from user.controllers import get_user_by_email

auth_handler = AuthProvider()


def register_user(user_model: SignUpRequestModel):
    user = get_user_by_email(user_model.email)
    if len(user) != 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists."
        )
    hashed_password = auth_handler.get_password_hash(user_model.password)
    query_put(
        """
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
            hashed_password,
        ),
    )
    return {
        "first_name": user_model.first_name,
        "last_name": user_model.last_name,
        "email": user_model.email,
        # Do not return the password hash or any sensitive information
    }


def signin_user(email, password):
    user = auth_handler.get_user_by_email(email)
    if len(user) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    elif not auth_handler.verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    del user["password_hash"]
    return user
