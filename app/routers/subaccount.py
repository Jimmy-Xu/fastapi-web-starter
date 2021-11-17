from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from binance import Client

from app.config import Config
import logging


router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/subaccount", response_class=HTMLResponse)
def get_subaccount(request: Request):
    tag = "flower"
    result = "Type a number"

    client = Client(Config.apiKey, Config.apiSecretKey)
    '''
    {
        "data": {
            "isLocked": false,
            "plannedRecoverTime": 0,
            "triggerCondition": {
                "UFR": 300,
                "IFER": 150,
                "GCR": 150
            },
            "updateTime": 1637078870786
        }
    }
    '''
    rlt = client.get_account_api_trading_status()
    logging.info(rlt)

    # sub_account_list = client.get_sub_account_list()
    sub_account_list = {
        "subAccounts": [
            {
                "email": "testsub@gmail.com",
                "isFreeze": False,
                "createTime": 1544433328000
            },
            {
                "email": "virtual@oxebmvfonoemail.com",
                "isFreeze": False,
                "createTime": 1544433328000
            }
        ]
    }

    fake_assets = {
        "testsub@gmail.com": {
            "balances": [
                {
                    "asset": "ADA",
                    "free": 10000,
                    "locked": 0
                },
                {
                    "asset": "BNB",
                    "free": 10003,
                    "locked": 0
                },
                {
                    "asset": "BTC",
                    "free": 11467.6399,
                    "locked": 0
                },
                {
                    "asset": "ETH",
                    "free": 10004.995,
                    "locked": 0
                },
                {
                    "asset": "USDT",
                    "free": 11652.14213,
                    "locked": 0
                }
            ],
        },
        "virtual@oxebmvfonoemail.com": {
            "balances": [
                {
                    "asset": "ADA",
                    "free": 20000,
                    "locked": 0
                },
                {
                    "asset": "BNB",
                    "free": 20003,
                    "locked": 0
                },
                {
                    "asset": "BTC",
                    "free": 21467.6399,
                    "locked": 0
                },
                {
                    "asset": "ETH",
                    "free": 20004.995,
                    "locked": 0
                },
                {
                    "asset": "USDT",
                    "free": 21652.14213,
                    "locked": 0
                }
            ],
        }
    }

    sub_account_assets = {}
    for item in sub_account_list['subAccounts']:
        # client.get_sub_account_assets(email=item['email'])
        sub_account_assets[item['email']] = fake_assets[item['email']]

    flora = ['aaa', 'bbb', 'ccc', 'ddd']
    fauna = ['111', '222', '333', '444']
    table = rlt['data']

    return templates.TemplateResponse(
        'subaccount.html',
        context={'request': request, 'result': result, 'tag': tag, 'flora': flora, 'fauna': fauna, 'table': table, 'sub_account_assets': sub_account_assets})


@router.post("/subaccount", response_class=HTMLResponse)
def post_subaccount(request: Request, tag: str = Form(...)):
    return templates.TemplateResponse('subaccount.html', context={'request': request, 'tag': tag})
