from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.commons.exceptions import AccessDeniedException
from app.models.user_model import User
from app.routers.constants import LOGIN_ENDPOINT
from app.security.token_factory import parse_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=LOGIN_ENDPOINT)


def authenticated(is_admin_required: bool = False):
    def check_permission(access_token: str = Depends(oauth2_scheme)) -> User:
        user = parse_access_token(access_token)
        if is_admin_required and not user.is_admin:
            raise AccessDeniedException("You're not authorized to perform this action")
        return user

    return check_permission
