from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime


class UserBaseModel(BaseModel):
    email: EmailStr


class CreateUserModel(UserBaseModel):
    password: str


class UpdateUserModel(UserBaseModel):
    password: str


class ResponseUserModel(UserBaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLoginModel(UserBaseModel):
    password: str


class PostBaseModel(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePostModel(PostBaseModel):
    pass


class UpdatePostModel(PostBaseModel):
    pass


class ResponsePostModel(PostBaseModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUserModel

    class Config:
        orm_mode = True


class ResponsePostVotesModel(BaseModel):
    Post: ResponsePostModel
    votes: int

    class Config:
        orm_mode = True


class AccessTokenModel(BaseModel):
    access_token: str
    token_type: str


class TokenDataModel(BaseModel):
    id: Optional[str]


class VoteModel(BaseModel):
    post_id: int
    dir: conint(le=1)
