from pydantic import BaseModel, validator, Field
from app.backend import utils
from fastapi import HTTPException, status


class NetworkTemplateBase(BaseModel):
    """shared properties"""

    network_template_name: str

    bandwidth_restriction_upload: float
    bandwidth_restriction_download: float

    dns_latency: float
    general_latency: float
    packet_loss: float


class NetworkTemplateIn(NetworkTemplateBase):
    """Properties to receive via API on creation base"""

    cidr_ip: str
    cidr_suffix: int = Field(ge=1, le=32)

    @validator("cidr_ip")
    @classmethod
    def validate_ip_cidr_notation(cls, v: str) -> str | None:
        """Custom validation to make sure cidr text is in proper format
        eg: 1.1.1.1/31
        """
        if utils.validate_ip_address_string(v):
            return v
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, f"'{v}' is not a valid ip address"
        )


class NetworkTemplateCreate(NetworkTemplateIn):
    """Properties to receive via API on creation"""


class NetworkTemplateUpdate(NetworkTemplateIn):
    """Properties to receive via API on updation"""


class NetworkTemplateOut(NetworkTemplateBase):
    """Additional properties to return via API"""

    no_of_pcs: int = 0
    cidr_notation: str

    class Config:
        orm_mode = True


class NetworkTemplateDBBase(NetworkTemplateBase):
    id: int | None = None


class NetworkTemplateInDB(NetworkTemplateDBBase):
    """Additional properties stored in DB"""

    no_of_pcs: int = 0
    cidr_notation: str
