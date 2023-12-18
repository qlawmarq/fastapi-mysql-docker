from fastapi import HTTPException, status
from database.connector import DatabaseConnector
from auth.provider import AuthProvider
from user.models import UserUpdateRequestModel

auth_handler = AuthProvider()

database = DatabaseConnector()


def update_user(user_model: UserUpdateRequestModel) -> int:
    # Check if the email is already in use by another user
    existing_user = get_users_by_email(user_model.email)
    if len(existing_user) != 0 and existing_user[0]["id"] != user_model.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already in use by another user",
        )
    # Before updating the password, check if it has been changed
    if user_model.password is not None and len(user_model.password) > 0:
        hashed_password = auth_handler.get_password_hash(user_model.password)
        # Update the user
        return database.query_put(
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
    else:
        # Update the user
        return database.query_put(
            """
                UPDATE user
                    SET first_name = %s,
                        last_name = %s,
                        email = %s
                    WHERE user.id = %s;
                """,
            (
                user_model.first_name,
                user_model.last_name,
                user_model.email,
                user_model.id,
            ),
        )


def get_all_users(limit: int = 10, offset: int = 0) -> list[dict]:
    users = database.query_get(
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
    return users


def get_users_by_email(email: str) -> list[dict]:
    users = database.query_get(
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
    return users


def get_user_by_id(id: int) -> dict:
    users = database.query_get(
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
    if len(users) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return users[0]
