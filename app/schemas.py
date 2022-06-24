from pydantic import BaseModel, EmailStr
from datetime import datetime


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

    class Config:
        orm_mode = True


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
