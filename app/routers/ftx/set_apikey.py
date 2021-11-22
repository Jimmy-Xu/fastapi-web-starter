import logging
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.models import api_keys
from app.models.posts import PostResponse
from app.security import manager
from app.db import get_session
from app.models.api_keys import ApiKeyResponse
from app.db.actions import create_api_key


router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/ftx/set_apikey", response_class=HTMLResponse)
def form_get(request: Request, user=Depends(manager)):
    logging.info(
        "receive GET /ftx/set_apikey, current user:{0}".format(user.username))

    apiKeyList = [ApiKeyResponse.from_orm(
        p) for p in user.api_keys if p.app_name == "ftx"]
    print("list api_keys: {0}".format(len(apiKeyList)))
    return templates.TemplateResponse('ftx/set_apikey.html', context={'request': request, 'result': apiKeyList})


@router.post("/ftx/set_apikey", response_class=HTMLResponse)
def create(request: Request, user=Depends(manager), db=Depends(get_session), api_key: str = Form(...), secret_key: str = Form(...)):
    logging.info(
        "receive POST /ftx/set_apikey: api_key={0}, secret_key={1}".format(api_key, secret_key))

    # add new post
    apiKey = create_api_key(
        app_name="ftx", api_key=api_key, secret_key=secret_key, owner=user, db=db)
    logging.info("new apiKey '{0}' added".format(apiKey.api_key))

    # add user to sesson again
    user = db.merge(user)

    # get new apiKeys
    apiKeyList = [ApiKeyResponse.from_orm(
        p) for p in user.api_keys if p.app_name == "ftx"]
    print("apiKeys after created: {0}".format(len(apiKeyList)))
    return templates.TemplateResponse('ftx/set_apikey.html', context={'request': request, 'result': apiKeyList})
