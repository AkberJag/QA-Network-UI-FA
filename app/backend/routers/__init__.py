from fastapi import APIRouter

from app.backend.core.config import settings

from . import auth
from . import public

frontend_routers = APIRouter(
    include_in_schema=settings.INCLUDE_FRONTEND_ENDPOINTS_IN_OpenAPI_SCHEMA
)

frontend_routers.include_router(auth.router)
frontend_routers.include_router(public.router)
