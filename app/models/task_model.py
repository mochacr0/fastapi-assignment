from sqlalchemy import Column, String, Enum, Uuid, ForeignKey
from sqlalchemy.orm import relationship

from app.commons.enums import TaskStatus, TaskPriority
from app.models.base_model import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"

    name = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), nullable=True)
    priority = Column(Enum(TaskPriority), nullable=True)
    assignee_id = Column(Uuid, ForeignKey("users.id"), nullable=True)
    assignee = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.name}>"
