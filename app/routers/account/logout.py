import logging
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.security import manager

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get('/account/logout', response_class=HTMLResponse)
def logout(request: Request, user=Depends(manager)):

    logging.info(
        "receive GET /account/logout, current user:{0}".format(user.username))

    resp = RedirectResponse(url="/login", status_code=302)
    manager.set_cookie(resp, "")
    return resp
