from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.commons.exceptions import (
    ResourceNotFoundException,
    UnprocessableEntityException,
)
from app.commons.utils import paginate
from app.models.task_model import Task
from app.models.user_model import User
from app.schemas.pagination_schema import (
    TaskPageParamsDto,
    PageData,
    MyTaskPageParamsDto,
)
from app.schemas.task_schema import CreateTaskDto, UpdateTaskDto
from app.services import auth_service, user_service


def find_tasks(db: Session, page_params: TaskPageParamsDto) -> PageData[Task]:
    query = db.query(Task)

    if page_params.assignee_id:
        query = query.filter(Task.assignee_id.__eq__(page_params.assignee_id))

    query = apply_common_filters(page_params, query)

    return paginate(query, page_params)


def find_my_tasks(
    db: Session, page_params: MyTaskPageParamsDto, security_user: User
) -> PageData[Task]:
    current_user = auth_service.get_current_user(security_user, db)
    query = db.query(Task).filter(Task.assignee_id.__eq__(current_user.id))

    query = apply_common_filters(page_params, query)

    return paginate(query, page_params)


def apply_common_filters(page_params, query):
    if page_params.text_search:
        query = query.filter(
            or_(
                Task.name.ilike(f"%{page_params.text_search}%"),
                Task.summary.ilike(f"%{page_params.text_search}%"),
                Task.description.ilike(f"%{page_params.text_search}%"),
            ),
        )

    if page_params.status:
        query = query.filter(Task.status == page_params.status)

    if page_params.priority:
        query = query.filter(Task.priority == page_params.priority)

    return query


def find_task_by_task_id(db: Session, task_id: UUID) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise ResourceNotFoundException("Task not found")
    return task


def create_task(db: Session, create_task_dto: CreateTaskDto) -> Task:
    task = Task(**create_task_dto.model_dump())

    if create_task_dto.assignee_id is not None:
        assignee = user_service.find_user_by_user_id(db, create_task_dto.assignee_id)
        if assignee is None:
            raise UnprocessableEntityException("Assignee not found")
        task.assignee = assignee

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: UUID, update_task_dto: UpdateTaskDto) -> Task:
    task = find_task_by_task_id(db, task_id)
    if (
        task.assignee_id != update_task_dto.assignee_id
        and update_task_dto.assignee_id is not None
    ):
        assignee = user_service.find_user_by_user_id(db, update_task_dto.assignee_id)
        if assignee is None:
            raise UnprocessableEntityException("Assignee not found")
        task.assignee_id = assignee.id
        task.assignee = assignee

    task.name = update_task_dto.name
    task.summary = update_task_dto.summary
    task.description = update_task_dto.description
    task.status = update_task_dto.status
    task.priority = update_task_dto.priority
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: UUID) -> None:
    try:
        task = find_task_by_task_id(db, task_id)
    except ResourceNotFoundException as ex:
        return None
    db.delete(task)
    db.commit()
    return None
