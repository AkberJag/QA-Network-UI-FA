from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend import dependencies
from app.backend.crud import crud_network_template
from app.backend.models import NetworkTemplate
from app.backend.schemas.network_template import (
    NetworkTemplateCreate,
    NetworkTemplateInDB,
    NetworkTemplateOut,
)

router = APIRouter()


@router.post("/", response_model=NetworkTemplateOut)
async def create_network_template(
    template_in: NetworkTemplateCreate, db: Session = Depends(dependencies.get_db)
):
    """Create new network template"""
    new_network_template = crud_network_template.get_by_template_name(
        db, template_in.network_template_name
    )

    if new_network_template:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This template name is already in use, choose a different name",
        )

    obj_in = NetworkTemplateInDB(**template_in.dict())
    return crud_network_template.create(db, obj_in)
