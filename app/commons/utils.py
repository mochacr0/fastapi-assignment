from math import ceil
from typing import TypeVar

from sqlalchemy import desc, asc
from sqlalchemy.orm import Query

from app.commons.enums import SortDirection
from app.configs.database import SessionLocal
from app.schemas.pagination_schema import PageParamsDto, PageData

T = TypeVar("T")


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def paginate(query: Query, page_params: PageParamsDto) -> PageData[T]:
    total_items = query.count()

    if page_params.sort_direction == SortDirection.DESC:
        final_query = query.order_by(desc(page_params.sort_property))
    else:
        final_query = query.order_by(asc(page_params.sort_property))

    final_query = final_query.limit(page_params.page_size).offset(
        page_params.page_size * page_params.page_number
    )

    query_results = final_query.all()
    total_pages = ceil(total_items / page_params.page_size)
    has_next = total_pages > page_params.page_number + 1
    return PageData(
        data=query_results,
        total_items=total_items,
        total_pages=total_pages,
        has_next=has_next,
    )
