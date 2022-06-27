from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import user, post, authentication, vote


app = FastAPI(
    title="posts-backend",
    version=2.0,
    root_path="/beta/")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
app.include_router(authentication.router)


@app.get('/')
async def root():
    return {'message': "Hello world!"}
