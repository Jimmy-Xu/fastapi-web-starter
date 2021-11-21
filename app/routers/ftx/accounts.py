from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from app.config import Config
import logging


router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/ftx/accounts", response_class=HTMLResponse)
def get_subaccount(request: Request):
    return templates.TemplateResponse(
        'ftx/accounts.html',
        context={'request': request})
