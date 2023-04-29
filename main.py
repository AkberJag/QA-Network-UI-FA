"""Main application package containing the app factory function."""

from fastapi import FastAPI

from app.backend.api.api_v1 import api


def create_application() -> FastAPI:
    """Create application factory something similar to the one used in Flask"""
    application = FastAPI()
    include_routers(application)
    return application


def include_routers(app: FastAPI):
    """Include FastAPI routers."""
    app.include_router(api.api_v1_router)


app = create_application()
