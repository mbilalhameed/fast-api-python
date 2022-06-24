import uvicorn

from fastapi import FastAPI

from . import models
from .database import engine
from .routers import user, post


app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)

models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def root():
    return {'message': "Hello world!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
