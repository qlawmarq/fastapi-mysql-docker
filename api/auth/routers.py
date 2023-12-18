from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from auth.provider import AuthProvider
from auth.controllers import (
    register_user,
    signin_user,
)
from auth.models import (
    UserAuthResponseModel,
    SignInRequestModel,
    SignUpRequestModel,
    AccessTokenResponseModel,
)

router = APIRouter()
auth_handler = AuthProvider()


@router.post("/v1/auth/signup", response_model=UserAuthResponseModel)
def signup_api(user_details: SignUpRequestModel):
    """
    This sign-up API allow you to register your account, and return access token.
    """
    user = register_user(user_details)
    access_token = auth_handler.encode_token(user_details.email)
    refresh_token = auth_handler.encode_refresh_token(user_details.email)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            {
                "token": {"access_token": access_token, "refresh_token": refresh_token},
                "user": user,
            }
        ),
    )


@router.post("/v1/auth/signin", response_model=UserAuthResponseModel)
def signin_api(user_details: SignInRequestModel):
    """
    This sign-in API allow you to obtain your access token.
    """
    user = signin_user(user_details.email, user_details.password)
    access_token = auth_handler.encode_token(user["email"])
    refresh_token = auth_handler.encode_refresh_token(user["email"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "token": {"access_token": access_token, "refresh_token": refresh_token},
                "user": user,
            }
        ),
    )


@router.post("/v1/auth/refresh-token", response_model=AccessTokenResponseModel)
def refresh_token_api(refresh_token: str):
    """
    This refresh-token API allow you to obtain new access token.
    """
    new_token = auth_handler.refresh_token(refresh_token)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"access_token": new_token}),
    )
