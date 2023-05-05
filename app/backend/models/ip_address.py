from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class IPAddress(Base):
    """An IP address with PC name and the network template"""

    id = Column(Integer, primary_key=True, index=True)

    pc_name = Column(String, unique=True)
    ip_address = Column(String, unique=True)

    networktemplates = relationship("NetworkTemplate", back_populates="ip_address_id")
    network_template_id = Column(Integer, ForeignKey("networktemplates.id"))
