from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.commons.utils import get_db_session
from app.models.user_model import User
from app.schemas.pagination_schema import PageDataDto, UserPageParamsDto
from app.schemas.user_schema import (
    UserDto,
    RegisterUserDto,
    UpdateUserDto,
    UserProfileDto,
)
from app.security.token_interceptor import authenticated
from app.services import user_service

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/", status_code=200, response_model=PageDataDto[UserDto])
def find_users(
    page_params_dto: UserPageParamsDto = Depends(),
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    return user_service.find_users(db, page_params_dto)


@user_router.get("/{userId}", status_code=200, response_model=UserDto)
def find_user_by_user_id(
    user_id: Annotated[UUID, Path(alias="userId")],
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    return user_service.find_user_by_user_id(db, user_id)


@user_router.post("/", status_code=201, response_model=UserDto)
def register_user(
    register_user_dto: RegisterUserDto,
    db: Session = Depends(get_db_session),
):
    return user_service.register_user(db, register_user_dto)


@user_router.put("/{userId}/disable", status_code=200, response_model=UserDto)
def disable_user(
    user_id: Annotated[UUID, Path(alias="userId")],
    db: Session = Depends(get_db_session),
    security_user: User = Depends(authenticated(is_admin_required=True)),
):
    return user_service.disable_user(db, user_id, security_user)


@user_router.put("/profile", status_code=200, response_model=UserProfileDto)
def update_profile(
    update_user_dto: UpdateUserDto,
    db: Session = Depends(get_db_session),
    security_user: User = Depends(authenticated()),
):
    return user_service.update_user(db, update_user_dto, security_user)


@user_router.delete("/{userId}", status_code=204)
def delete_user(
    user_id: Annotated[UUID, Path(alias="userId")],
    db: Session = Depends(get_db_session),
    security_user: User = Depends(authenticated(is_admin_required=True)),
):
    return user_service.delete_user(db, user_id, security_user)
