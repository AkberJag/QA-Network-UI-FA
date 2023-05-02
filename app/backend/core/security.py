"""Security utilities.

Includes:

* Authentication mechanisms:
    * OAuth2 with Password (and hashing), Bearer with JWT tokens.

* Password Hashing: includes utilities to hash passwords using multiple hashing algorithms, with a secure salt.
* Password Verification: includes utilities to verify passwords that were hashed with multiple algorithms (to migrate old hashed passwords).
* OAuth2 scopes: includes utilities to define OAuth2 scopes, check if they are included in a token, etc.
"""

from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from app.backend.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"])
ALGORITHM: str = "HS256"


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    """Create the jwt token for a user"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_password(password: str, hashed_password: str) -> bool:
    """Match the password against a hash"""
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)
