from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.param_functions import Depends

from app.config import Config
import logging

from app.library.helpers import get_default_api_keys
from app.security import manager

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/ftx/accounts", response_class=HTMLResponse)
def get_accounts(request: Request, user=Depends(manager)):
    logging.info(
        "receive GET /ftx/accounts: user={0}".format(user.username))

    apiKey, secretKey = get_default_api_keys(
        user.api_keys,  Config.ctrKey, 'ftx', user.username)
    if apiKey is None or secretKey is None:
        logging.error(
            "failed to get default api key for user {0}".format(user.uesrname))
        return

    # logging.debug(
    #     "found default api key({0}/{1}) for user {2}".format(apiKey, secretKey, user.username))

    all_balances = {}
    error = ""
    try:

        # for debug
        all_balances = {
            "success": True,
            "result": {
                "main": [
                    {"coin": "USDTBEAR", "free": 2320.2, "spotBorrow": 0.0, "total": 2340.2,
                        "usdValue": 2340.2, "availableWithoutBorrow": 2320.2},
                    {"coin": "BTC", "free": 2.0, "spotBorrow": 0.0, "total": 3.2,
                        "usdValue": 23456.7, "availableWithoutBorrow": 2.0}
                ],
                "Battle Royale": [
                    {"coin": "USD", "free": 2000.0, "spotBorrow": 0.0, "total": 2200.0,
                        "usdValue": 2200.0, "availableWithoutBorrow": 2000.0}
                ]
            }
        }
    except Exception as e:
        logging.error(
            "failed to get sub account assets, error:{0}".format(str(e)))
        error = "failed to get sub account assets, internal server error"
    finally:
        return templates.TemplateResponse(
            'ftx/accounts.html',
            context={'request': request, 'all_balances': all_balances, 'error': error})
