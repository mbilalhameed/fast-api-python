from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()
my_posts = []


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


@app.get('/')
async def root():
    return {'message': "Hello world!"}


@app.get('/posts')
def get_posts():
    return {'data': ['post1', 'post2', 'post3']}


@app.post('/post')
def create_post(post: Post):
    post = post.dict()
    post['id'] = len(my_posts) + 1

    my_posts.append(post)

    return {
        'message': "post created successfully",
        "post": post
    }
