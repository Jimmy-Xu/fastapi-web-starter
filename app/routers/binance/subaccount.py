from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.param_functions import Depends

from app.config import Config
from app.security import manager
from app.library.helpers import get_default_api_keys, is_dev_mode

import os
import logging
from binance import Client


router = APIRouter(
    prefix="/binance"
)
templates = Jinja2Templates(directory="templates/")


@router.get("/subaccount", response_class=HTMLResponse)
def get_subaccount(request: Request, user=Depends(manager)):

    dev_mode = is_dev_mode()
    logging.info(
        "receive GET /binance/subaccount: user={0}, dev_mode={1}".format(user.username, dev_mode))

    # get default binance api key
    apiKey, secretKey = get_default_api_keys(
        user.api_keys,  Config.ctrKey, 'binance', user.username)
    if apiKey is None or secretKey is None:
        logging.error(
            "failed to get default api key for user {0}".format(user.uesrname))
        return

    # logging.debug(
    #     "found default api key({0}/{1}) for user {2}".format(apiKey, secretKey, user.username))

    client = Client(api_key=apiKey, api_secret=secretKey, testnet=False)

    sub_account_assets = {}
    error = ""
    try:

        if not dev_mode:
            sub_account_assets = client.get_sub_account_assets()
        else:
            # for debug
            sub_account_assets = {
                "testsub@gmail.com": {
                    "balances": [
                        {"asset": "ADA", "free": 10000, "locked": 0},
                        {"asset": "BNB", "free": 10003, "locked": 0},
                        {"asset": "BTC", "free": 11467.6399, "locked": 0},
                        {"asset": "ETH", "free": 10004.995, "locked": 0},
                        {"asset": "USDT", "free": 11652.14213, "locked": 0}],
                },
                "virtual@oxebmvfonoemail.com": {
                    "balances": [
                        {"asset": "ADA", "free": 20000, "locked": 0},
                        {"asset": "BNB", "free": 20003, "locked": 0},
                        {"asset": "BTC", "free": 21467.6399, "locked": 0},
                        {"asset": "ETH", "free": 20004.995, "locked": 0},
                        {"asset": "USDT", "free": 21652.14213, "locked": 0}],
                }
            }
    except Exception as e:
        logging.error(
            "failed to get sub account assets, error:{0}".format(str(e)))
        error = "failed to get sub account assets, internal server error"
    finally:
        return templates.TemplateResponse(
            'binance/subaccount.html',
            context={'request': request, 'sub_account_assets': sub_account_assets, 'error': error})
