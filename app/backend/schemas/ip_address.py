"""Ip address pydantic schema"""

from pydantic import BaseModel


class IPAddressBase(BaseModel):
    """shared properties"""

    pc_name: str
    ip_address: str
    network_template_id: int


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
