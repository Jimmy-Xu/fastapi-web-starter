from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.library.helpers import openfile
from app.routers.auth.forms import LoginForm
#from fastapi import Depends
#from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    print("get login page")
    return templates.TemplateResponse("login.html", context={"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    print("receive login request")
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("login.html", form.__dict__)
            #login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Username or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)