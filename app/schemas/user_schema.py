from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as PydanticSchema

from app.schemas.company_schema import CompanyDto, UserCompanyDto


class UserDto(PydanticSchema):
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    company: UserCompanyDto | None = None

    class Config:
        orm_mode = True


class UserProfileDto(PydanticSchema):
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str


class TaskUserDto(PydanticSchema):
    id: UUID
    username: str
    first_name: str
    last_name: str


class RegisterUserDto(PydanticSchema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    company_id: UUID


# class SecurityUser:
#     username: str
#     is_admin: bool


class UpdateUserDto(PydanticSchema):
    first_name: str
    last_name: str
