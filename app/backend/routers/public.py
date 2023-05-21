from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.backend.models import User
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

    return template.TemplateResponse(
        "public/home.html", {"request": request, "current_user": current_user}
    )
