from typing import Generator

from fastapi import Depends, HTTPException, status
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


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_barer)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from exc
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid input",
        ) from exc

    user = crud_user.get(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
