from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.dependencies import get_db
from app.backend.crud import crud_ip_address, crud_network_template
from app.backend.models.ip_address import IPAddress
from app.backend.schemas.ip_address import IPAddressOut, IPAddressCreate, IPAddressInDB
from app.backend.core.database import update_pc_count

router = APIRouter()


@router.get("/", response_model=list[IPAddressOut])
async def get_all_ip_address(db: Session = Depends(get_db)) -> list[IPAddressOut]:
    """Return all ip address"""
    return db.query(IPAddress).all()


@router.post("/", response_model=IPAddressOut)
async def create_new_ip(ip_address_in: IPAddressCreate, db: Session = Depends(get_db)):
    """Create new IP address"""

    network_template = crud_network_template.get(db, ip_address_in.network_template_id)
    if not network_template:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Selected network template does not exist"
        )

    ip_address = crud_ip_address.get_by_pc_name(db, ip_address_in.pc_name)
    if ip_address:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This ip address name is already in use, choose a different name",
        )
    ip_address = crud_ip_address.get_by_ip_address(db, ip_address_in.ip_address)
    if ip_address:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This ip address already added",
        )

    obj_in = IPAddressInDB(**ip_address_in.dict())
    new_ip_address = crud_ip_address.create(db, obj_in)
    update_pc_count(db, new_ip_address.network_template_id)
    return new_ip_address


@router.put("/{ip_address_id}", response_model=IPAddressOut)
async def edit_ip_address(
    ip_address_in: IPAddressCreate, ip_address_id: int, db: Session = Depends(get_db)
):
    ip_address_to_update = crud_ip_address.get(db, ip_address_id)
    if not ip_address_to_update:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Selected Ip Addess/Pc does not exist"
        )
    old_template_id = ip_address_to_update.network_template_id

    ip_address = (
        db.query(IPAddress)
        .filter(IPAddress.pc_name == ip_address_in.pc_name)
        .filter(IPAddress.id != ip_address_id)
        .first()
    )
    if ip_address:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This ip address name is already in use, choose a different name",
        )

    ip_address = (
        db.query(IPAddress)
        .filter(IPAddress.ip_address == ip_address_in.ip_address)
        .filter(IPAddress.id != ip_address_id)
        .first()
    )
    if ip_address:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This ip address already added",
        )

    obj_in = IPAddressInDB(**ip_address_in.dict())
    updated_ip = crud_ip_address.update(db, obj_in, ip_address_to_update)
    update_pc_count(db, ip_address_in.network_template_id, old_template_id)

    return updated_ip
