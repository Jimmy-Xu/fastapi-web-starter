import datetime
from pydantic import BaseModel


class ApiKeyCreate(BaseModel):
    app_name: str
    api_key: str
    secret_key: str


class ApiKeyResponse(ApiKeyCreate):
    '''
    fix: none is not an allowed value
    '''
    #created_at: datetime.datetime

    class Config:
        orm_mode = True
