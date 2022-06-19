from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()


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


@app.post('/createpost')
def create_post(post: Post):
    print(post.rating)
    return {
        'message': "post created successfully",
        "post_title": f"{post.title}",
        "post_content": f"{post.content}",
        "publish_post": f"{post.publish}"
    }
