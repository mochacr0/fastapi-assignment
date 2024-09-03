from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.commons.exceptions import ResourceNotFoundException, UnauthorizedException
from app.commons.utils import get_db_session
from app.configs.app_settings import bcrypt_context
from app.models.user_model import User
from app.routers.constants import LOGIN_ENDPOINT
from app.schemas.token_schema import TokenDto
from app.schemas.user_schema import UserDto, UserProfileDto
from app.security.token_factory import create_access_token
from app.security.token_interceptor import authenticated
from app.services import auth_service, user_service

auth_router = APIRouter(tags=["Auth"])


@auth_router.post(LOGIN_ENDPOINT, status_code=200, response_model=TokenDto)
def login(
    login_dto: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db_session),
):
    user: User
    try:
        user = user_service.find_user_by_username(db, login_dto.username)
    except ResourceNotFoundException:
        raise UnauthorizedException("Invalid username or password")
    if not bcrypt_context.verify(login_dto.password, user.hashed_password):
        raise UnauthorizedException("Invalid username or password")
    if not user.is_active:
        raise UnauthorizedException("User is disabled")
    return create_access_token(user)


@auth_router.get("/auth/current", status_code=200, response_model=UserProfileDto)
def get_current_user(
    security_user: User = Depends(authenticated()),
    db: Session = Depends(get_db_session),
):
    return auth_service.get_current_user(security_user, db)
