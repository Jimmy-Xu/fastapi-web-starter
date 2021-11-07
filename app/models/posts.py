import datetime
from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str


class PostResponse(PostCreate):
    '''
    fix: none is not an allowed value
    '''
    #created_at: datetime.datetime

    class Config:
        orm_mode = True
