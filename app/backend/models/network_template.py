from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class NetworkTemplate(Base):
    """A network template where different parameters of a network is configured"""

    network_template_name = Column(String, unique=True)  # Eg: good network

    cidr_notation = Column(String)  # Eg: 192.168.1.1/23

    bandwidth_restriction_upload = Column(Float)
    bandwidth_restriction_download = Column(Float)

    dns_latency = Column(Float)
    general_latency = Column(Float)
    packet_loss = Column(Float)

    # this is to hold the total number of pcs configured for a template
    # ? Question: is this a better way or joining 2 tables and counting is better?
    no_of_pcs = Column(Integer, default=0)

    ip_address_id = relationship(
        "IPAddress",
        back_populates="networktemplates",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
