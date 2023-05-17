from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.backend.models import User
from app.backend.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["auth"])
template = Jinja2Templates(directory="app/frontend/templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return template.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    # user: User = Depends(get_current_user)
    user = 1
    return template.TemplateResponse(
        "auth/register.html", {"request": request, "user": user}
    )
