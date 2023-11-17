from fastapi import HTTPException, status
from database.query import query_get, query_put
from auth.provider import AuthProvider
from user.models import UserUpdateRequestModel

auth_handler = AuthProvider()


def update_user(user_model: UserUpdateRequestModel):
    # Check if the email is already in use by another user
    existing_user = get_user_by_email(user_model.email)
    if existing_user and existing_user.id != user_model.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already in use by another user",
        )
    # Update the user
    hashed_password = auth_handler.get_password_hash(user_model.password)
    return query_put(
        """
            UPDATE user
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    password_hash = %s
                WHERE user.id = %s;
            """,
        (
            user_model.first_name,
            user_model.last_name,
            user_model.email,
            hashed_password,
            user_model.id,
        ),
    )


def get_all_users(limit: int = 10, offset: int = 0):
    user = query_get(
        """
        SELECT
            user.id,
            user.first_name,
            user.last_name,
            user.email
        FROM user
        LIMIT %s OFFSET %s
        """,
        (limit, offset),
    )
    return user


def get_user_by_email(email: str):
    user = query_get(
        """
        SELECT
            user.id,
            user.first_name,
            user.last_name,
            user.email
        FROM user
        WHERE email = %s
        """,
        (email),
    )
    return user


def get_user_by_id(id: int):
    user = query_get(
        """
        SELECT
            user.id,
            user.first_name,
            user.last_name,
            user.email
        FROM user
        WHERE id = %s
        """,
        (id),
    )
    return user
