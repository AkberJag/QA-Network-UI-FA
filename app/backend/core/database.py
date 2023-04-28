"""DB Session"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.backend.core import config


# database engine that is used to interact with the database.
engine = create_engine(
    config.settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)

# a class that provides a thread-local session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
