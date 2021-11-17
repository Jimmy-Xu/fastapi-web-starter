from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

import logging
from app.config import Config


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

    flora = ['aaa', 'bbb', 'ccc', 'ddd']
    fauna = ['111', '222', '333', '444']
    table = rlt['data']

    return templates.TemplateResponse(
        'subaccount.html',
        context={'request': request, 'result': result, 'tag': tag, 'flora': flora, 'fauna': fauna, 'table': table})


@router.post("/subaccount", response_class=HTMLResponse)
def post_subaccount(request: Request, tag: str = Form(...)):
    return templates.TemplateResponse('subaccount.html', context={'request': request, 'tag': tag})
