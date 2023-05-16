from fastapi import APIRouter

from . import auth

frontend_routers = APIRouter()
frontend_routers.include_router(auth.router)
