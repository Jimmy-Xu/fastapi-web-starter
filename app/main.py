from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

import jwt
import logging
from .library.helpers import *

from app.routers.auth import login
from app.routers.auth.auth import router as auth_router
from app.routers.auth.user import router as user_router
from app.security import manager
from app.config import Config

from app.routers.binance import subaccount as binance_subaccount
from app.routers.binance import apikey as binance_apikey
from app.routers.ftx import accounts as ftx_accounts
from app.routers.ftx import apikey as ftx_apikey
from app.routers.account import resetpwd as account_resetpwd
from app.routers.account import logout as account_logout
from fastapi.param_functions import Depends


logging.basicConfig(
    level=logging.DEBUG,              # 定义输出到文件的log级别，
    # 定义输出log的格式
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',                                     # 时间
    # filename = logFilename,                # log文件名
    # filemode = 'w'                        # 写入模式“w”或“a”
)


app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login.router)
app.include_router(auth_router)
app.include_router(user_router)

# binance api
app.include_router(binance_subaccount.router)
app.include_router(binance_apikey.router)
# ftx api
app.include_router(ftx_accounts.router)
app.include_router(ftx_apikey.router)
# account
app.include_router(account_resetpwd.router)
app.include_router(account_logout.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request,  user=Depends(manager)):
    return templates.TemplateResponse("home.html", {"request": request, 'username': user.username})


# https://github.com/MushroomMaula/fastapi_login/issues/28
@app.middleware("http")
async def redirect_middleware(request: Request, call_next):
    whitelist = ['/login', '/static']
    # non authenticated path
    logging.info(
        "redirect_middleware: request.url.path={0}".format(request.url.path))
    url_prefix = "/{0}".format(request.url.path.split("/")[1])
    if url_prefix in whitelist:
        return await call_next(request)
    else:
        # Expired token redirects back to login page.
        cookie = request.cookies.get(manager.cookie_name)
        logging.info("cookie:{0}".format(cookie))
        if cookie:
            try:
                logging.info("check cooke wether expired")
                jwt.decode(str(request.cookies.get(manager.cookie_name)),
                           Config.secret, algorithms=["HS256"])
            except jwt.ExpiredSignatureError as e:
                logging.info("check cooke already expired, goto login page")
                return RedirectResponse(url='/login')
            else:
                return await call_next(request)
        else:
            logging.info("cooke not found, goto login page")
            return RedirectResponse(url='/login')
