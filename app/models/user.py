from typing import List
from pydantic import BaseModel

from app.models.posts import PostResponse
from app.models.api_keys import ApiKeyResponse


class UserCreate(BaseModel):
    username: str
    password: str


class UserReponse(UserCreate):

    posts: List[PostResponse]
    api_keys: List[ApiKeyResponse]

    class Config:
        orm_mode = True
