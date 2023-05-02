from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.backend import dependencies
from app.backend.schemas import UserCreate, UserOut
from app.backend.core import security

from app.backend.models import User

from app.backend.crud.crud_user import crud_user

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserCreate, db: Session = Depends(dependencies.get_db)):
    """Create new user"""

    user = crud_user.get_by_email(db, user_in.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email is already in use"
        )

    obj_in = User(
        **user_in.dict(exclude={"password"}),
        hashed_password=security.get_password_hash(user_in.password)
    )

    return crud_user.create(db, obj_in)
