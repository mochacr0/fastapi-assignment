from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as PydanticSchema

from app.commons.enums import TaskStatus, TaskPriority
from app.schemas.user_schema import TaskUserDto


class TaskDto(PydanticSchema):
    id: UUID
    name: str
    summary: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    assignee: TaskUserDto | None = None

    class Config:
        orm_mode = True


class SaveTaskDto(PydanticSchema):
    name: str
    summary: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: UUID | None = None


class CreateTaskDto(SaveTaskDto):
    pass


class UpdateTaskDto(SaveTaskDto):
    pass
