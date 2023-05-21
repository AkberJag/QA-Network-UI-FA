from typing import Generator

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.backend.core.database import SessionLocal
from app.backend.core.config import settings
from app.backend.core import security

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
        user_id: int | None = payload.get("sub")

        return {"id": user_id, "msg": "Success"}
    except:
        return {
            "id": None,
            "msg": "Could not validate credentials",
        }
