import logging
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.security import manager
from app.db.actions import reset_user_pwd
from app.db import get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/account/resetpwd", response_class=HTMLResponse)
def form_get(request: Request, db=Depends(get_session), user=Depends(manager)):
    logging.info(
        "receive GET /account/resetpwd, current user:{0}".format(user.username))

    return templates.TemplateResponse('account/resetpwd.html', context={'request': request, 'error': '', 'password0': '', 'password1': '', 'password2': ''})


@router.post("/account/resetpwd", response_class=HTMLResponse)
def form_get(request: Request, user=Depends(manager), db=Depends(get_session), password0: str = Form(...), password1: str = Form(...), password2: str = Form(...)):
    logging.info(
        "receive POST /account/resetpwd, current user:{0}, password1:{1}, password2:{2}".format(user.username, password1, password2))

    error = ""
    if password0 == password1:
        error = "Password not change!"
    elif password1 != password2:
        error = "Passwords not match!"
    else:
        ok, error = reset_user_pwd(user.username, password0, password1, db)
        if ok:
            resp = RedirectResponse(url="/login", status_code=302)
            manager.set_cookie(resp, "")
            return resp

    return templates.TemplateResponse('account/resetpwd.html', context={'request': request, 'error': error, 'password0': password0, 'password1': password1, 'password2': password2})
