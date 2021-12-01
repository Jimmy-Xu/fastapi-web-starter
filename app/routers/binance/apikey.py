import logging
from fastapi import Request, Form, APIRouter
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

router = APIRouter(
    prefix="/binance"
)
templates = Jinja2Templates(directory="templates/")


@router.get("/apikey", response_class=HTMLResponse)
def get(request: Request, user=Depends(manager)):

    logging.info(
        "receive GET /binance/apikey, current user:{0}".format(user.username))

    apiKeyList = mask_api_keys(user.api_keys, Config.ctrKey, 'binance')

    print("found api_keys: {0}".format(len(apiKeyList)))

    return templates.TemplateResponse('binance/apikey.html', context={'request': request, 'result': apiKeyList})


@router.post("/apikey", response_class=HTMLResponse)
def create(request: Request, user=Depends(manager), db=Depends(get_session), api_key: str = Form(...), secret_key: str = Form(...)):

    logging.info(
        "receive POST /binance/apikey: api_key={0}, secret_key(plain)={1}".format(api_key, mask_text(secret_key)))

    # save current api key list
    apiKeyList = mask_api_keys(user.api_keys, Config.ctrKey, 'binance')

    # add new api key
    apiKey, err = create_api_key(
        app_name="binance", api_key=api_key, secret_key=aes_encrypt(secret_key, Config.ctrKey), owner=user, db=db)
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
        apiKeyList = mask_api_keys(user.api_keys, Config.ctrKey, 'binance')

    return templates.TemplateResponse('binance/apikey.html', context={'request': request, 'result': apiKeyList, 'api_key': api_key, 'secret_key': secret_key,  'error': err})


@router.delete("/apikey/{apikey}")
def delete(apikey: str, user=Depends(manager), db=Depends(get_session)):
    logging.info(
        "receive DELETE /binance/apikey/{0}".format(apikey))
    try:
        # delete api key
        delete_api_key(
            app_name="binance", api_key=apikey, owner=user, db=db)
        logging.info("binance API Key '{0}' was deleted".format(apikey))
    except Exception as e:
        logging.error(
            "failed to delete binance API Key {0}, error: {1}".format(apikey, str(e)))


@router.post("/apikey/set_default")
def set_default(apikey: str, user=Depends(manager), db=Depends(get_session)):
    logging.info(
        "receive POST /binance/apikey/set_default: api_key={0}".format(apikey))
    try:
        # set default api key
        set_default_api_key(app_name="binance",
                            api_key=apikey, owner=user, db=db)
        logging.info("binance API Key '{0}' was set as default".format(apikey))
    except Exception as e:
        logging.error(
            "failed to set binance API Key {0} as default, error: {1}".format(apikey, str(e)))
