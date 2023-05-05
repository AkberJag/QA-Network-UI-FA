"""Ip address pydantic schema"""

from pydantic import BaseModel


class IPAddressBase(BaseModel):
    """shared properties"""

    pc_name: str
    ip_address: str


class IPAddressCreate(IPAddressBase):
    """Properties to recive when a new ip is created"""

    network_template_id: int


class IPAddressOut(IPAddressBase):
    """Additional properties to return via API"""

    class Config:
        orm_mode = True
