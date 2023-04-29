"""Application Configuration."""

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """App settings"""

    API_V1_URL: str = "/api/v1"
    SECRET_KEY: str = "SuperSecretKey"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # create the db folder to avoid the error > sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
    if not os.path.exists(os.path.join(BASE_DIR, "dbs")):
        os.makedirs(os.path.join(BASE_DIR, "dbs"))

    DB_FOLDER = os.path.join(BASE_DIR, "dbs")
    DB_NAME = "dev.sqlite"
    DB_PATH = os.path.join(DB_FOLDER, DB_NAME)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


settings = Settings()
