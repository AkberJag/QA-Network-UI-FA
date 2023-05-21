from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.backend.models import User, IPAddress, NetworkTemplate
from app.backend.crud import crud_network_template
from app.backend.dependencies import get_db

from . import route_dependencies

router = APIRouter()
template = Jinja2Templates(directory="app/frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    current_user: User = Depends(route_dependencies.get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.get("id"):
        return RedirectResponse("/user/logout")

    network_templates = crud_network_template.get_all(db)

    templates = {}
    for nw_template in network_templates:
        templates[nw_template.id] = {
            "pc": (
                db.query(IPAddress, NetworkTemplate)
                .select_from(IPAddress)
                .join(NetworkTemplate)
                .filter(IPAddress.network_template_id == nw_template.id)
                .all()
            ),
            "template": nw_template,
        }

    return template.TemplateResponse(
        "public/home.html",
        {"request": request, "current_user": current_user, "templates": templates},
    )
