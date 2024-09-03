from sqlalchemy import Column, String, Boolean, Uuid, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="true")
    is_admin = Column(Boolean, nullable=False, server_default="false")
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="users")
    tasks = relationship("Task", back_populates="assignee")

    def __repr__(self):
        return f"<User {self.username}>"
