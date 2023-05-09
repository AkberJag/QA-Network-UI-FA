from fastapi import APIRouter
from app.backend.api.api_v1.endpoints import login, users, network_template
from app.backend.core.config import settings

api_v1_router = APIRouter(prefix=settings.API_V1_URL)
api_v1_router.include_router(login.router, tags=["login"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
api_v1_router.include_router(
    network_template.router, prefix="/network_template", tags=["network_template"]
)
