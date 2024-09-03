from fastapi import Depends
from sqlalchemy.orm import Session

from app.commons.exceptions import UnauthorizedException
from app.commons.utils import get_db_session
from app.models.user_model import User


def get_current_user(
    security_user: User, db: Session = Depends(get_db_session)
) -> User:
    from app.services import user_service

    user = user_service.find_user_by_username(db, security_user.username)
    if user is None:
        raise UnauthorizedException("Your account cannot be found")
    if not user.is_active:
        raise UnauthorizedException("Your account is disabled")
    return user
