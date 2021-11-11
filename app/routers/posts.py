import logging
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.models.posts import PostResponse
from app.security import manager
from app.db import get_session
from app.models.posts import PostCreate, PostResponse
from app.db.actions import create_post, get_user_by_name


router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/posts", response_class=HTMLResponse)
def form_get(request: Request, user=Depends(manager)):
    logging.info("receive GET /posts, current user:{0}".format(user.username))

    postList = [PostResponse.from_orm(p) for p in user.posts]
    print("list posts: {0}".format(len(postList)))
    return templates.TemplateResponse('posts.html', context={'request': request, 'result': postList})


@router.post("/posts", response_class=HTMLResponse)
def create(request: Request, user=Depends(manager), db=Depends(get_session), text: str = Form(...)):
    logging.info("receive POST /posts: text={0}".format(text))

    # add new post
    post = create_post(text, user, db)
    logging.info("new post '{0}' added".format(post.text))

    # add user to sesson again
    user = db.merge(user)

    # get new posts
    postList = [PostResponse.from_orm(p) for p in user.posts]
    print("posts after created: {0}".format(len(postList)))
    return templates.TemplateResponse('posts.html', context={'request': request, 'result': postList})
