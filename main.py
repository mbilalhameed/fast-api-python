from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()
my_posts = []


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


def find_post(post_id):
    for post in my_posts:
        if post['id'] == post_id:
            return post


def remove_post(post_id):
    if not my_posts:
        return None, False

    for index, post in enumerate(my_posts):
        if post['id'] == post_id:
            my_posts.pop(index)

            return post, True

    return None, False


def update_post(post_id, new_data):
    if not my_posts:
        return None, False

    for post in my_posts:
        if post['id'] == post_id:
            post['title'] = new_data.title
            post['content'] = new_data.content
            post['publish'] = new_data.publish
            post['rating'] = new_data.rating

            return post, True

    return None, False


@app.get('/')
async def root():
    return {'message': "Hello world!"}


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


@app.post('/post', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.dict()
    post['id'] = len(my_posts) + 1

    my_posts.append(post)

    return {
        'message': "Post created successfully",
        "post": post
    }


@app.get('post/latest')
def get_latest_post():
    if my_posts:
        post = my_posts[-1]

        return {
            "message": "Latest post fetched successfully",
            "post": post
        }

    else:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There are no posts")


@app.get('post/{id}')
def get_post(post_id: int):
    post = find_post(post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={post_id} doesn't exist'")

    return {
        "message": "Post fetched successfully",
        "post": post
    }


@app.delete('post/delete/{id}', status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    post, removed = remove_post(post_id)

    if not removed:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('post/{id}')
def update_post(post_id: int, post: Post):
    post, updated = update_post(post_id, post)

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={post_id} doesn't exist'")

    return {
        "message": "Post updated successfully",
        "post": post
    }
