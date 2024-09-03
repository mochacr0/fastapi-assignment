from uuid import UUID

from sqlalchemy.orm import Session

from app.commons.exceptions import (
    UnprocessableEntityException,
    ResourceNotFoundException,
    InvalidDataException,
)
from app.commons.utils import paginate
from app.configs.app_settings import bcrypt_context
from app.models.user_model import User
from app.schemas.pagination_schema import PageParamsDto, PageData, UserPageParamsDto
from app.schemas.user_schema import RegisterUserDto, UpdateUserDto
from app.services import company_service
from app.services.auth_service import get_current_user


def find_users(db: Session, page_params: UserPageParamsDto) -> PageData[User]:
    query = db.query(User)
    if page_params.company_id:
        query = query.filter(User.company_id == page_params.company_id)
    if page_params.is_active is not None:
        query = query.filter(User.is_active == page_params.is_active)
    if page_params.is_admin is not None:
        query = query.filter(User.is_admin == page_params.is_admin)
    if page_params.text_search:
        query = query.filter(
            User.username.ilike(f"%{page_params.text_search}%")
            | User.first_name.ilike(f"%{page_params.text_search}%")
            | User.last_name.ilike(f"%{page_params.text_search}%")
            | User.email.ilike(f"%{page_params.text_search}%")
        )
    return paginate(query, page_params)


def find_user_by_user_id(db: Session, user_id: UUID) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ResourceNotFoundException("User not found")
    return user


def find_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ResourceNotFoundException("User not found")
    return user


def register_user(db: Session, register_user_dto: RegisterUserDto) -> User:
    duplicated_username_user = (
        db.query(User).filter(User.username == register_user_dto.username).first()
    )
    if duplicated_username_user:
        raise InvalidDataException("Username is already taken")

    duplicated_email_user = (
        db.query(User).filter(User.email == register_user_dto.email).first()
    )
    if duplicated_email_user:
        raise InvalidDataException("Email already exists")

    try:
        company = company_service.find_company_by_company_id(
            db, register_user_dto.company_id
        )
    except ResourceNotFoundException as ex:
        raise UnprocessableEntityException(ex.detail)

    user = User(**register_user_dto.model_dump(exclude={"password"}))
    user.hashed_password = bcrypt_context.hash(register_user_dto.password)
    user.company = company
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def disable_user(db: Session, user_id: UUID, security_user: User) -> User:
    user = find_user_by_user_id(db, user_id)
    current_user = get_current_user(security_user, db)
    if user.id == current_user.id:
        raise InvalidDataException("You cannot disable yourself")
    if user.is_admin:
        raise InvalidDataException("You cannot disable an admin user")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def update_user(
    db: Session, update_user_dto: UpdateUserDto, security_user: User
) -> User:
    user = get_current_user(security_user, db)
    user.first_name = update_user_dto.first_name
    user.last_name = update_user_dto.last_name
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: UUID, security_user: User) -> None:
    user: User | None = None
    try:
        user = find_user_by_user_id(db, user_id)
    except ResourceNotFoundException as ex:
        pass
    current_user = get_current_user(security_user, db)
    if user.id == current_user.id:
        raise InvalidDataException("You cannot delete yourself")
    if user.is_admin:
        raise InvalidDataException("You cannot delete an admin user")
    if user.tasks and len(user.tasks) > 0:
        raise InvalidDataException("User has tasks, cannot be deleted")
    db.delete(user)
    db.commit()
