from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.commons.utils import get_db_session
from app.schemas.company_schema import CreateCompanyDto, UpdateCompanyDto, CompanyDto
from app.schemas.pagination_schema import (
    PageDataDto,
    CompanyPageParamsDto,
)
from app.security.token_interceptor import authenticated
from app.services import company_service

company_router = APIRouter(prefix="/companies", tags=["Company"])


@company_router.get("/", status_code=200, response_model=PageDataDto[CompanyDto])
def find_companies(
    page_params_dto: CompanyPageParamsDto = Depends(),
    db: Session = Depends(get_db_session),
    _=Depends(authenticated()),
):
    result = company_service.find_companies(db, page_params_dto)
    return result


@company_router.get("/{companyId}", status_code=200, response_model=CompanyDto)
def find_company_by_company_id(
    company_id: Annotated[UUID, Path(alias="companyId")],
    db: Session = Depends(get_db_session),
    _=Depends(authenticated()),
):
    return company_service.find_company_by_company_id(db, company_id)


@company_router.post("/", status_code=201, response_model=CompanyDto)
def create_company(
    create_company_dto: CreateCompanyDto,
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    return company_service.create_company(db, create_company_dto)


@company_router.put("/{companyId}", status_code=200, response_model=CompanyDto)
def update_company(
    company_id: Annotated[UUID, Path(alias="companyId")],
    update_company_dto: UpdateCompanyDto,
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    return company_service.update_company(db, company_id, update_company_dto)


@company_router.delete("/{companyId}", status_code=204)
def delete_company(
    company_id: Annotated[UUID, Path(alias="companyId")],
    db: Session = Depends(get_db_session),
    _=Depends(authenticated(is_admin_required=True)),
):
    company_service.delete_company(db, company_id)
    return None
