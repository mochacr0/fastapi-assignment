from dotenv import load_dotenv
from sqlalchemy import create_engine, DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import expression

from app.configs.app_settings import app_settings

load_dotenv()


class UtcNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UtcNow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def get_connection_url() -> str:
    return (
        f"{app_settings.DATABASE_SCHEME}://{app_settings.DATABASE_USERNAME}"
        f":{app_settings.DATABASE_PASSWORD}@{app_settings.DATABASE_HOST}"
        f":{app_settings.DATABASE_PORT}/{app_settings.DATABASE_NAME}"
    )


SQLALCHEMY_DATABASE_URL = get_connection_url()
db_engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
