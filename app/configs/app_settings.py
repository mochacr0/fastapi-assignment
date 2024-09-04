from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class AppSettings(BaseSettings):
    DATABASE_SCHEME: str = "postgresql"
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "localhost"
    DATABASE_NAME: str = "fastapi_db"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_IN_MINUTES: int = 30
    DEFAULT_USER_PASSWORD: str = "string"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_settings = AppSettings()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
