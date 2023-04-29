from typing import Generator

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.backend.core.database import SessionLocal
from app.backend.core.config import settings

oauth2_barer = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_URL}/login/token")


def get_db() -> Generator:
    """Create a new database session and close it when the request is complete"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
