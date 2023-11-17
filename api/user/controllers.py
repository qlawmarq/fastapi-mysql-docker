from fastapi import HTTPException
from database.query import query_get, query_put
from auth.provider import Auth
from user.models import UserUpdateRequestModel

auth_handler = Auth()


def update_user(user_model: UserUpdateRequestModel):
    hashed_password = auth_handler.encode_password(user_model.password)
    query_put(
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
    user = get_user_by_id(user_model.id)
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]


def get_all_users():
    user = query_get(
        """
        SELECT
            user.id,
            user.first_name,
            user.last_name,
            user.email
        FROM user
        """,
        (),
    )
    return user


def get_user_by_email(email: str):
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
            user.email,
        FROM user
        WHERE id = %s
        """,
        (id),
    )
    return user
