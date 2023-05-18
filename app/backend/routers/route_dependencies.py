from typing import Generator

from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.backend.core.database import SessionLocal
from app.backend.core.config import settings
from app.backend.core import security
from app.backend.models import User
from app.backend import schemas
from app.backend.crud import crud_user

oauth2_barer = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_URL}/login/token")


def get_db() -> Generator:
    """Create a new database session and close it when the request is complete"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        user_id: int | None = payload.get("id")

        if None in (username, user_id):
            await logout(request)
        return {"username": username, "id": user_id}
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from exc
