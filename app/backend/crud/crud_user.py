from sqlalchemy.orm import Session

from app.backend.models import User
from app.backend.schemas import UserCreate, UserUpdate
from app.backend.core import security

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """User specific crud opertations"""

    def get_by_email(self, db: Session, email: str) -> None | User:
        """Return a user object by email adderss"""
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, email: str, password: str):
        """Authenticate a user is the provided password is correct"""
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user


curd_user = CRUDUser(User)
