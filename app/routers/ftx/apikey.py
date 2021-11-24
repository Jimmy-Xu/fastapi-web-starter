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


router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/ftx/apikey", response_class=HTMLResponse)
def form_get(request: Request, user=Depends(manager)):
    logging.info(
        "receive GET /ftx/apikey, current user:{0}".format(user.username))

    apiKeyList = mask_api_keys(user.api_keys, Config.ctrKey, 'ftx')

    print("list api_keys: {0}".format(len(apiKeyList)))
    return templates.TemplateResponse('ftx/apikey.html', context={'request': request, 'result': apiKeyList})


@router.post("/ftx/apikey", response_class=HTMLResponse)
def create(request: Request, user=Depends(manager), db=Depends(get_session), api_key: str = Form(...), secret_key: str = Form(...)):
    logging.info(
        "receive POST /ftx/apikey: api_key={0}, secret_key(plain)={1}".format(api_key, mask_text(secret_key)))

    # save current api key list
    apiKeyList = mask_api_keys(user.api_keys, Config.ctrKey, 'ftx')

    # add new api key
    apiKey, err = create_api_key(
        app_name="ftx", api_key=api_key, secret_key=aes_encrypt(secret_key, Config.ctrKey), owner=user, db=db)
    if err != None:
        logging.error(
            "failed to add new apiKey '{0}', error: {1}".format(api_key, err))
        if "UNIQUE constraint failed" in err:
            err = "api_key '{0}' duplicated".format(api_key)
        else:
            err = "failed to add API KEY {0}".format(api_key)
    else:
        logging.info("new apiKey '{0}' added".format(apiKey.api_key))
        # add user to sesson again
        user = db.merge(user)
        # get new apiKeys
        apiKeyList = mask_api_keys(user.api_keys, Config.ctrKey, 'ftx')

    return templates.TemplateResponse('ftx/apikey.html', context={'request': request, 'result': apiKeyList, 'api_key': api_key, 'secret_key': secret_key,  'error': err})


@router.delete("/ftx/apikey/{apikey}")
def create(apikey: str, user=Depends(manager), db=Depends(get_session)):
    logging.info(
        "receive DELETE /ftx/apikey: api_key={0}".format(apikey))
    try:
        # delete api key
        delete_api_key(
            app_name="ftx", api_key=apikey, owner=user, db=db)
        logging.info("ftx API Key '{0}' was deleted".format(apikey))
    except Exception as e:
        logging.error(
            "failed to delete ftx API Key {0}, error: {1}".format(apikey, str(e)))


@router.post("/ftx/apikey/set_default")
def set_default(apikey: str, user=Depends(manager), db=Depends(get_session)):
    logging.info(
        "receive POST /ftx/apikey/set_default: api_key={0}".format(apikey))
    try:
        # set default api key
        set_default_api_key(app_name="ftx",
                            api_key=apikey, owner=user, db=db)
        logging.info("ftx API Key '{0}' was set as default".format(apikey))
    except Exception as e:
        logging.error(
            "failed to set ftx API Key {0} as default, error: {1}".format(apikey, str(e)))
