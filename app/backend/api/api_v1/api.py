from fastapi import APIRouter
from app.backend.api.api_v1.endpoints import login, users, network_template, ip_address
from app.backend.core.config import settings

api_v1_router = APIRouter(prefix=settings.API_V1_URL)
api_v1_router.include_router(login.router, tags=["Login"])
api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(
    network_template.router, prefix="/network_template", tags=["Network Template"]
)

api_v1_router.include_router(
    ip_address.router, prefix="/ip_address", tags=["Ip Address"]
)
