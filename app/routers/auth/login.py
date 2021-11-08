import logging
from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers.auth.forms import LoginForm


from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from app.db import get_session
from app.db.actions import get_user_by_name
from app.models.auth import Token
from app.security import verify_password, manager
from starlette.responses import RedirectResponse


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    print("get login page")
    return templates.TemplateResponse("login.html", context={"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_session)):
    print("receive login request")
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = None
            access_token, err = login_for_access_token(form=form, db=db)
            if err:
                # raise InvalidCredentialsException
                form.__dict__.update(msg="")
                form.__dict__.get("errors").append(err)
                response = templates.TemplateResponse(
                    "login.html", form.__dict__)
            else:
                form.__dict__.update(msg="Login Successful :)")
                form.__dict__.update(errors=[])
                response = templates.TemplateResponse(
                    "login.html", form.__dict__)
                response.set_cookie(
                    key=manager.cookie_name,
                    value=f"Bearer {access_token}",
                    httponly=True,
                    max_age=2147483647,
                    expires=2147483647,
                )
                logging.info("user {0} login successful".format(form.username))
            return response
        except HTTPException as e:
            logging.error("HTTPException: {0}".format(str(e)))
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append(str(e))
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


def login_for_access_token(form, db):
    user = get_user_by_name(form.username, db)
    if user is None:
        logging.info("username {0} not found".format(form.username))
        return None, "Incorrect Username or Password"

    logging.info("username {0} found".format(form.username))
    if not verify_password(form.password, user.password):
        logging.error("invalid password of username {0}".format(form.username))
        return None, "Incorrect Username or Password"

    access_token = manager.create_access_token(data={'sub': user.username})
    return access_token, None
