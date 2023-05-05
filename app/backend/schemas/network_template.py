from pydantic import BaseModel


class NetworkTemplateBase(BaseModel):
    """shared properties"""

    network_template_name: str

    cidr_notation: str

    bandwidth_restriction_upload: float
    bandwidth_restriction_download: float

    dns_latency: float
    general_latency: float
    packet_loss: float


class NetworkTemplateCreate(NetworkTemplateBase):
    """Properties to receive via API on creation"""

    no_of_pcs: int = 0


class NetworkTemplateUpdate(NetworkTemplateBase):
    """Properties to receive via API on creation"""


class NetworkTemplateOut(NetworkTemplateBase):
    """Additional properties to return via API"""

    class Config:
        orm_mode = True
