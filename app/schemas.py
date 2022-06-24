from pydantic import BaseModel


class PostBaseModel(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePostModel(PostBaseModel):
    pass


class UpdatePostModel(PostBaseModel):
    pass
