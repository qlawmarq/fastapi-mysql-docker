from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from auth.provider import AuthProvider, AuthUser
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
auth_handler = AuthProvider()


@router.get("/v1/users", response_model=list[UserResponseModel])
def get_all_users_api(
    current_user: AuthUser = Depends(auth_handler.get_current_user),
):
    """
    This users get API allow you to fetch all user data.
    """
    user = get_all_users()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))


@router.get("/v1/user/{user_id}", response_model=UserResponseModel)
def get_user_api(
    user_id: int,
    current_user: AuthUser = Depends(auth_handler.get_current_user),
):
    """
    This user API allow you to fetch specific user data.
    """
    user = get_user_by_id(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))


@router.put("/v1/user/{user_id}", response_model=UserResponseModel)
def update_user_api(
    user_id: int,
    user_details: UserUpdateRequestModel,
    current_user: AuthUser = Depends(auth_handler.get_current_user),
):
    """
    This user update API allow you to update user data.
    """
    update_user(user_details)
    user = get_user_by_id(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
