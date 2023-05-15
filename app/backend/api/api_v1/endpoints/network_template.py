from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend import dependencies
from app.backend.crud import crud_network_template
from app.backend.models import NetworkTemplate, User
from app.backend.schemas.network_template import (
    NetworkTemplateCreate,
    NetworkTemplateInDB,
    NetworkTemplateOut,
)

router = APIRouter()


@router.post("/", response_model=NetworkTemplateOut)
async def create_network_template(
    template_in: NetworkTemplateCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.get_current_user),
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

    obj_in = NetworkTemplateInDB(
        **template_in.dict(),
        cidr_notation=f"{template_in.cidr_ip}/{template_in.cidr_suffix}",
    )
    return crud_network_template.create(db, obj_in)


@router.put("/{template_id}/", response_model=NetworkTemplateOut)
async def edit_template(
    template_id: int,
    template_in: NetworkTemplateCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> NetworkTemplateOut:
    """Edit a template"""

    template = crud_network_template.get(db, template_id)

    if not template:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Network template not found"
        )

    if (
        db.query(NetworkTemplate)
        .filter(
            NetworkTemplate.network_template_name == template_in.network_template_name
        )
        .filter(NetworkTemplate.id != template_id)
        .first()
    ):
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="This template name is already in use, choose a different name",
        )

    obj_in = NetworkTemplateInDB(
        **template_in.dict(),
        cidr_notation=f"{template_in.cidr_ip}/{template_in.cidr_suffix}",
    )
    return crud_network_template.update(db, obj_in, template)


@router.delete("/{template_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.get_current_user),
):
    template = crud_network_template.get(db, template_id)

    if not template:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail="Network template not found"
        )
    crud_network_template.delete(db, template_id)


@router.get("/", response_model=list[NetworkTemplateOut])
async def return_all_templates(
    db: Session = Depends(dependencies.get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> list[NetworkTemplateOut] | None:
    """Return all available network templates"""

    return db.query(NetworkTemplate).all()
