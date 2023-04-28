from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    """User Model"""

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
