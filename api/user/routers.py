from fastapi import APIRouter, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from auth.provider import Auth
from user.controllers import (
    update_user,
    get_all_users,
    get_user_by_id,
)
from user.models import (
    UserUpdateRequestModel,
    UserResponseModel,
)

router = APIRouter()
OAuth2 = HTTPBearer()
auth_handler = Auth()


@router.get("/v1/users", response_model=list[UserResponseModel])
def get_all_users_api(credentials: HTTPAuthorizationCredentials = Security(OAuth2)):
    """
    This users get API allow you to fetch all user data.
    """
    token = credentials.credentials
    if auth_handler.decode_token(token):
        user = get_all_users()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "Failed to authorize"})
    )


@router.get("/v1/user/{user_id}", response_model=UserResponseModel)
def get_user_api(
    user_id: int, credentials: HTTPAuthorizationCredentials = Security(OAuth2)
):
    """
    This user API allow you to fetch specific user data.
    """
    token = credentials.credentials
    if auth_handler.decode_token(token):
        user = get_user_by_id(user_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "Failed to authorize"})
    )


@router.post("/v1/user/update", response_model=UserResponseModel)
def update_user_api(
    user_details: UserUpdateRequestModel,
    credentials: HTTPAuthorizationCredentials = Security(OAuth2),
):
    """
    This user update API allow you to update user data.
    """
    token = credentials.credentials
    if auth_handler.decode_token(token):
        user = update_user(user_details)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content=jsonable_encoder({"error": "Failed to authorize"})
    )
