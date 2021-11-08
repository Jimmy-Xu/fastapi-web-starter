import logging
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.models.posts import PostResponse
from app.models.user import UserReponse
from app.security import manager
from app.db import get_session


router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/posts", response_class=HTMLResponse)
def form_get(request: Request, user=Depends(manager)):
    logging.info("receive GET /posts, current user:{0}".format(user.username))

    postList = [PostResponse.from_orm(p) for p in user.posts]
    print("posts: {0}".format(len(postList)))
    return templates.TemplateResponse('posts.html', context={'request': request, 'result': postList})


@router.post("/posts", response_class=HTMLResponse)
def form_post1(request: Request, text: int = Form(...)):
    return templates.TemplateResponse('posts.html', context={'request': request, 'result': text})
