from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.backend.crud import crud_user
from app.backend import dependencies
from app.backend.core import security
from app.backend.core.config import settings

router = APIRouter()


@router.post("/login/token")
async def login_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """OAuth2 compatible token login, get an access token for future requests"""
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    token_expires = timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(user.id, token_expires)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
