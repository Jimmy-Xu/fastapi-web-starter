from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *

from app.routers.auth import login
from app.routers.auth.auth import router as auth_router
from app.routers.auth.user import router as user_router
from app.routers.auth.posts import router as posts_router
from app.routers import twoforms, unsplash, accordion, posts

import logging

logging.basicConfig(
    level    = logging.DEBUG,              # 定义输出到文件的log级别，                                                            
    format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',    # 定义输出log的格式
    datefmt  = '%Y-%m-%d %H:%M:%S',                                     # 时间
    #filename = logFilename,                # log文件名
    #filemode = 'w'                        # 写入模式“w”或“a”
)


app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login.router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(posts_router)


app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)
app.include_router(posts.router)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
