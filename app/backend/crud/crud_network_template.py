from sqlalchemy.orm import Session

from app.backend.schemas.network_template import (
    NetworkTemplateBase,
    NetworkTemplateCreate,
    NetworkTemplateUpdate,
)
from .base import CRUDBase
from app.backend.models.network_template import NetworkTemplate


class CURDNetworkTemplate(
    CRUDBase[NetworkTemplate, NetworkTemplateCreate, NetworkTemplateUpdate]
):
    def get_by_template_name(
        self, db: Session, template_name: str
    ) -> None | NetworkTemplate:
        """Return a network template object by the template name"""
        return (
            db.query(NetworkTemplate)
            .filter(NetworkTemplate.network_template_name == template_name)
            .first()
        )


crud_network_template = CURDNetworkTemplate(NetworkTemplate)
