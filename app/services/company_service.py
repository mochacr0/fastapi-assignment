from uuid import UUID

from sqlalchemy.orm import Session

from app.commons.exceptions import ResourceNotFoundException, InvalidDataException
from app.commons.utils import paginate
from app.models.company_model import Company
from app.schemas.company_schema import CreateCompanyDto, UpdateCompanyDto
from app.schemas.pagination_schema import PageData, CompanyPageParamsDto


def find_companies(db: Session, page_params: CompanyPageParamsDto) -> PageData[Company]:
    query = db.query(Company)
    if page_params.text_search:
        query = query.filter(Company.name.ilike(f"%{page_params.text_search}%"))
    return paginate(query, page_params)


def find_company_by_company_id(db: Session, company_id: UUID) -> Company:
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise ResourceNotFoundException("Company not found")
    return company


def create_company(db: Session, create_company_dto: CreateCompanyDto) -> Company:
    duplicated_name_company = (
        db.query(Company).filter(Company.name == create_company_dto.name).first()
    )
    if duplicated_name_company:
        raise InvalidDataException("Company with this name already exists")
    company = Company(**create_company_dto.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def update_company(
    db: Session, company_id: UUID, update_company_dto: UpdateCompanyDto
) -> Company:
    company = find_company_by_company_id(db, company_id)
    if update_company_dto.name != company.name:
        duplicated_name_company = (
            db.query(Company).filter(Company.name == update_company_dto.name).first()
        )
        if duplicated_name_company:
            raise InvalidDataException("Company with this name already exists")
    company.name = update_company_dto.name
    company.description = update_company_dto.description
    company.mode = update_company_dto.mode
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company_id: UUID) -> None:
    try:
        company = find_company_by_company_id(db, company_id)
    except ResourceNotFoundException:
        return None
    if company.users and len(company.users) > 0:
        raise InvalidDataException("Company has users, cannot be deleted")
    db.delete(company)
    db.commit()
    return None
