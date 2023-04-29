from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.backend.crud import curd_user
from app.backend import dependencies

router = APIRouter()


@router.post("/login/token")
async def login_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """OAuth2 compatible token login, get an access token for future requests"""
    user = curd_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
