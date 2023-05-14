from sqlalchemy.orm import Session

from app.backend.models.ip_address import IPAddress
from app.backend.schemas import ip_address

from .base import CRUDBase


class CURDIpAddress(
    CRUDBase[IPAddress, ip_address.IPAddressCreate, ip_address.IPAddressUpdate]
):
    def get_by_pc_name(self, db: Session, pc_name: str) -> None | IPAddress:
        return db.query(IPAddress).filter(IPAddress.pc_name == pc_name).first()

    def get_by_ip_address(self, db: Session, ip_address: str) -> None | IPAddress:
        return db.query(IPAddress).filter(IPAddress.ip_address == ip_address).first()


crud_ip_address = CURDIpAddress(IPAddress)
