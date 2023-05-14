from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.dependencies import get_db
from app.backend.crud import crud_ip_address
from app.backend.models.ip_address import IPAddress
from app.backend.schemas.ip_address import IPAddressOut, IPAddressCreate, IPAddressInDB

router = APIRouter()


@router.get("/", response_model=list[IPAddressOut])
async def get_ip_address(db: Session = Depends(get_db)) -> list[IPAddressOut]:
    return db.query(IPAddress).all()


@router.post("/", response_model=IPAddressOut)
async def create_new_ip(ip_address_in: IPAddressCreate, db: Session = Depends(get_db)):
    """Create new IP address"""
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
            detail="This ip address already in added",
        )

    obj_in = IPAddressInDB(**ip_address_in.dict())
    return crud_ip_address.create(db, obj_in)
