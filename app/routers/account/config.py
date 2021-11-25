import logging
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.config import Config
from app.security import manager
from app.db import get_session
from app.db.actions import create_api_key, delete_api_key, set_default_api_key

from app.library.helpers import mask_api_keys, aes_encrypt, mask_text

from binance import Client

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/account/resetpwd", response_class=HTMLResponse)
def form_get(request: Request, user=Depends(manager)):
    logging.info(
        "receive GET /binance/apikey, current user:{0}".format(user.username))

    return templates.TemplateResponse('account/resetpwd.html', context={'request': request})
