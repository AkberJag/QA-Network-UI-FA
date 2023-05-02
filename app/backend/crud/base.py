from typing import TypeVar, Type, Generic

from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.backend.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchematype = TypeVar("UpdateSchematype", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchematype]):
    """Base crud class"""

    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def create(self, db: Session, obj_in: CreateSchemaType) -> None | ModelType:
        """Adds a new object to the database and returns the object with the new ID."""
        # todo: make this async
        obj_in_data = self.model(**obj_in.dict())
        db.add(obj_in_data)
        db.commit()
        db.refresh(obj_in_data)
        return obj_in_data

    def get(self, db: Session, id: int) -> None | ModelType:
        """Retrieves an object from the database by its ID"""
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, obj_in: UpdateSchematype):
        """Updates an existing object in the database"""
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def delete(self, db: Session, id: int):
        """Delete an object from the db"""
        obj = db.query(self.model).get(id)
        try:
            db.delete(obj)
            db.commit()
        finally:
            return obj
