from fastapi import APIRouter

from app.routers.auth_router import auth_router
from app.routers.company_router import company_router
from app.routers.task_router import task_router
from app.routers.user_router import user_router

app_router = APIRouter()
app_router.include_router(task_router)
app_router.include_router(company_router)
app_router.include_router(auth_router)
app_router.include_router(user_router)
