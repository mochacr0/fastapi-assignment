from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.commons.utils import get_db_session
from app.models.user_model import User
from app.schemas.pagination_schema import (
    TaskPageParamsDto,
    PageDataDto,
    MyTaskPageParamsDto,
)
from app.schemas.task_schema import TaskDto, CreateTaskDto, UpdateTaskDto
from app.security.token_interceptor import authenticated
from app.services import task_service

task_router = APIRouter(prefix="/tasks", tags=["Task"])


@task_router.get("/", status_code=200, response_model=PageDataDto[TaskDto])
def find_tasks(
    page_params_dto: TaskPageParamsDto = Depends(),
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    return task_service.find_tasks(db, page_params_dto)


@task_router.get("/my-tasks", status_code=200, response_model=PageDataDto[TaskDto])
def find_my_tasks(
    page_params_dto: MyTaskPageParamsDto = Depends(),
    db: Session = Depends(get_db_session),
    security_user: User = Depends(authenticated()),
):
    return task_service.find_my_tasks(db, page_params_dto, security_user)


@task_router.get("/{taskId}", status_code=200, response_model=TaskDto)
def find_task_by_task_id(
    task_id: Annotated[UUID, Path(alias="taskId")],
    db: Session = Depends(get_db_session),
    _=Depends(authenticated()),
):
    return task_service.find_task_by_task_id(db, task_id)


@task_router.post("/", status_code=201, response_model=TaskDto)
def create_task(
    create_task_dto: CreateTaskDto,
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    return task_service.create_task(db, create_task_dto)


@task_router.put("/{taskId}", status_code=200, response_model=TaskDto)
def update_task(
    task_id: Annotated[UUID, Path(alias="taskId")],
    update_task_dto: UpdateTaskDto,
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    return task_service.update_task(db, task_id, update_task_dto)


@task_router.delete("/{taskId}", status_code=204)
def delete_task(
    task_id: Annotated[UUID, Path(alias="taskId")],
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    task_service.delete_task(db, task_id)
    return None
