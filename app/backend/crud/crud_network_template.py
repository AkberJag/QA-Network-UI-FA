from app.backend.schemas.network_template import (
    NetworkTemplateBase,
    NetworkTemplateCreate,
    NetworkTemplateUpdate,
)
from .base import CRUDBase
from app.backend.models.network_template import NetworkTemplate

CURDNetworkTemplate = CRUDBase[
    NetworkTemplateBase, NetworkTemplateCreate, NetworkTemplateUpdate
]
crud_network_template = CURDNetworkTemplate(NetworkTemplate)
