from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.backend.dependencies import get_db
from .route_dependencies import get_current_user
from app.backend.crud import crud_user
from app.backend.schemas import UserInDB
from app.backend.core import security

router = APIRouter(prefix="/user", tags=["auth"])
template = Jinja2Templates(directory="app/frontend/templates")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return template.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return template.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_post(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()

    validate_email = crud_user.get_by_email(db, form_data.get("email"))

    if validate_email:
        return template.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "msg": "This email is already in use",
                "category": "danger",
            },
        )

    obj_in = UserInDB(
        email=form_data.get("email"),
        hashed_password=security.get_password_hash(form_data.get("password")),
    )

    crud_user.create(db, obj_in)

    return RedirectResponse(url="login", status_code=status.HTTP_302_FOUND)


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
