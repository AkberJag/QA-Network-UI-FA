"""Ip address pydantic schema"""

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from app.backend.dependencies import get_db
from app.backend.models import NetworkTemplate
from app.backend import utils


class IPAddressBase(BaseModel):
    """shared properties"""

    pc_name: str
    ip_address: str
    network_template_id: int

    @validator("ip_address")
    @classmethod
    def validate_ip_address(cls, v: str) -> str | None:
        """Custom validation to make sure the given ip addess is a valid ip address"""
        if utils.validate_ip_address_string(v):
            return v
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, f"'{v}' is not a valid ip address"
        )


class IPAddressCreate(IPAddressBase):
    """Properties to recive when a new ip is created"""


class IPAddressUpdate(IPAddressBase):
    """Properties to recive when a new ip is updated"""


class IPAddressOut(IPAddressBase):
    """Additional properties to return via API"""

    class Config:
        orm_mode = True


class IPAddressDBBase(IPAddressBase):
    id: int | None = None


class IPAddressInDB(IPAddressDBBase):
    """Additional properties stored in DB"""
