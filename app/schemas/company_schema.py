from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as PydanticSchema

from app.commons.enums import CompanyMode


class CompanyDto(PydanticSchema):
    id: UUID
    name: str
    description: str
    mode: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserCompanyDto(PydanticSchema):
    id: UUID
    name: str


class SaveCompanyDto(PydanticSchema):
    name: str
    description: str
    mode: CompanyMode | None = None


class CreateCompanyDto(SaveCompanyDto):
    pass


class UpdateCompanyDto(SaveCompanyDto):
    pass
