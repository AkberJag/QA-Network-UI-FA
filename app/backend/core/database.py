"""DB Session"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.backend.core import config
from app.backend.models import IPAddress, NetworkTemplate
from app.backend.crud import crud_network_template
from app.backend.schemas import NetworkTemplateUpdate


# database engine that is used to interact with the database.
engine = create_engine(
    config.settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)

# a class that provides a thread-local session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def update_pc_count(
    db: Session,
    new_template_id: int,
    old_template_id: int | None = None,
) -> None:
    """Update the 'no_of_pcs' column on a network tempate table

    Args:
        new_template_id: Network template's PK
        old_template_id: to decrement one from the current template when the template of an ip address is changed
    """
    network_template: NetworkTemplate = crud_network_template.get(db, new_template_id)
    network_template.no_of_pcs = len(
        db.query(NetworkTemplate, IPAddress)
        .select_from(IPAddress)
        .join(NetworkTemplate)
        .filter(IPAddress.network_template_id == new_template_id)
        .all()
    )
    crud_network_template.update(
        db, NetworkTemplateUpdate(**network_template.__dict__), network_template
    )

    if old_template_id:
        network_template: NetworkTemplate = crud_network_template.get(
            db, old_template_id
        )
        network_template.no_of_pcs = len(
            db.query(NetworkTemplate, IPAddress)
            .select_from(IPAddress)
            .join(NetworkTemplate)
            .filter(IPAddress.network_template_id == old_template_id)
            .all()
        )
    crud_network_template.update(
        db, NetworkTemplateUpdate(**network_template.__dict__), network_template
    )
