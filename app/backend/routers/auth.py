from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.backend.models import User
from .route_dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["auth"])
template = Jinja2Templates(directory="app/frontend/templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return template.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return template.TemplateResponse("auth/register.html", {"request": request})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    user = await get_current_user(request)

    if not user:
        return RedirectResponse(url="/register", status_code=status.HTTP_302_FOUND)

    msg = "Logged out!"

    response = template.TemplateResponse(
        "auth/login.html",
        {"request": request, "msg": msg},
        status_code=status.HTTP_302_FOUND,
    )
    response.delete_cookie(key="access_token")
    return response
