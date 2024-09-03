from typing import TypeVar, Generic

from pydantic import BaseModel as PydanticSchema, Field

from app.commons.enums import SortDirection, TaskStatus, TaskPriority

T = TypeVar("T")


class PageDataDto(PydanticSchema, Generic[T]):
    total_pages: int
    total_items: int
    has_next: bool
    data: list[T]


class PageData(Generic[T]):
    def __init__(
        self, data: list[T], total_items: int, total_pages: int, has_next: bool
    ):
        self.data = data
        self.total_items = total_items
        self.total_pages = total_pages
        self.has_next = has_next


class PageParamsDto(PydanticSchema):
    page_number: int = Field(
        ge=0,
        default=0,
        description="Page number must be greater than 0",
        alias="pageNumber",
    )
    page_size: int = Field(
        ge=0,
        default=10,
        description="Page size must be greater than 0",
        alias="pageSize",
    )
    sort_property: str = Field(
        default="created_at", description="Sort property", alias="sortProperty"
    )
    sort_direction: SortDirection = Field(
        default=SortDirection.ASC, description="Sort direction", alias="sortDirection"
    )


class CompanyPageParamsDto(PageParamsDto):
    text_search: str | None = Field(default=None, description="Company name")


class BaseTaskPageParamsDto(PageParamsDto):
    text_search: str | None = Field(
        default=None, description="Task name, summary or description"
    )
    status: TaskStatus | None = Field(default=None, description="Task status")
    priority: TaskPriority | None = Field(default=None, description="Task priority")


class TaskPageParamsDto(BaseTaskPageParamsDto):
    assignee_id: str | None = Field(default=None, description="Assignee ID")


class MyTaskPageParamsDto(BaseTaskPageParamsDto):
    pass


class UserPageParamsDto(PageParamsDto):
    company_id: str | None = Field(default=None, description="Company ID")
    is_active: bool | None = Field(default=None, description="Is active")
    is_admin: bool | None = Field(default=None, description="Is admin")
    text_search: str | None = Field(
        default=None, description="Username, email or full name"
    )
