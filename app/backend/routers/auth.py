from datetime import timedelta

from fastapi import APIRouter, Request, status, Depends, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.backend.dependencies import get_db
from .route_dependencies import get_current_user
from app.backend.crud import crud_user
from app.backend.schemas import UserInDB
from app.backend.core import security

router = APIRouter(prefix="/user", tags=["auth"])
template = Jinja2Templates(directory="app/frontend/templates")


class LoginForm:
    def __init__(self, request: Request) -> None:
        self.request = request
        self.username: str | None = None
        self.password: str | None = None
        self.errors: list

    async def create_oauth_form(self):
        form = await self.request.form()

        self.username = form.get("email")
        self.password = form.get("password")


async def login_for_access_token(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        return False

    token_expires = timedelta(minutes=30)
    token = security.create_access_token(user_id=user.id, expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request, current_user: Session = Depends(get_current_user)):
    if current_user.get("id"):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return template.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    if current_user.get("id"):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response, db, form)
        if not validate_user_cookie:
            msg = "Incorrect Username or password"
            return template.TemplateResponse(
                "auth/login.html", {"request": request, "msg": msg}
            )
        return response
    except HTTPException:
        msg = "unknown error"
        return templates.TemplateResponse(
            "auth/login.html", {"request": request, "msg": msg}
        )


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request, current_user: Session = Depends(get_current_user)):
    if current_user.get("id"):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return template.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    if current_user.get("id"):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
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
    print(user)

    if not user.get("id"):
        return RedirectResponse(url="/user/login", status_code=status.HTTP_302_FOUND)

    msg = "Logged out!"

    response = template.TemplateResponse(
        "auth/login.html",
        {"request": request, "msg": msg},
        status_code=status.HTTP_302_FOUND,
    )
    response.delete_cookie(key="access_token")
    return response
