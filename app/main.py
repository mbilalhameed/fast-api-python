from typing import Optional

import psycopg2
import uvicorn
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

app = FastAPI()
my_posts = []

try:
    conn = psycopg2.connect(
        host='localhost',
        database='fastapi',
        user='postgres',
        password='admin0336',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database was connected successfully ")
except Exception as error:
    print("Failed to connect to Database")
    print(error.args)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/')
async def root():
    return {'message': "Hello world!"}


@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return {'data': posts}


@app.post('/create/post', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.dict()
    # print(post)
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
        RETURNING  *;""",
        (post['title'], post['content'], post['published'])
    )
    new_post = cursor.fetchone()
    conn.commit()

    return {
        'message': "Post created successfully",
        "post": new_post
    }


@app.get('/fetch/post/{id}')
def get_post(id: str):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (id, ))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} doesn't exist'")

    return {
        "message": "Post fetched successfully",
        "post": post
    }


@app.get('/fetch/latest/post')
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


@app.delete('/delete/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (id, ))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/update/post/{id}')
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s RETURNING *;""",
        (post.title, post.content, post.published)
    )

    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} doesn't exist'")

    return {
        "message": "Post updated successfully",
        "post": updated_post
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
