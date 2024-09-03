from datetime import datetime, timezone, timedelta

import jwt
from jwt import InvalidTokenError

from app.commons.exceptions import BadCredentialsException
from app.configs.app_settings import app_settings
from app.models.user_model import User
from app.schemas.token_schema import TokenDto


def create_access_token(user: User) -> TokenDto:
    claims = {"sub": user.username, "is_admin": user.is_admin}

    token_expires = datetime.now(timezone.utc) + timedelta(
        app_settings.JWT_ACCESS_TOKEN_EXPIRE_IN_MINUTES
    )

    access_token = jwt.encode(
        {"exp": token_expires, **claims},
        app_settings.JWT_SECRET_KEY,
        algorithm=app_settings.JWT_ALGORITHM,
    )

    return TokenDto(access_token=access_token, token_type="bearer")


def parse_access_token(access_token: str) -> User:
    try:
        payload = jwt.decode(
            access_token,
            app_settings.JWT_SECRET_KEY,
            algorithms=[app_settings.JWT_ALGORITHM],
        )
    except InvalidTokenError as ex:
        raise BadCredentialsException(f"Invalid access token: {ex}")

    username = payload.get("sub")
    if username is None:
        raise BadCredentialsException("Invalid access token: Missing subject")

    user = User()
    user.username = username
    user.is_admin = payload.get("is_admin", False)
    return user
