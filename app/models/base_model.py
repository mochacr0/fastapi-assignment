import uuid

from sqlalchemy import Column, DateTime, Uuid
from sqlalchemy.orm import declarative_base

from app.configs.database import UtcNow

SQLAlchemyBaseModel = declarative_base()


class BaseModel(SQLAlchemyBaseModel):
    __abstract__ = True

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=UtcNow())
    updated_at = Column(DateTime, server_default=UtcNow(), onupdate=UtcNow())
