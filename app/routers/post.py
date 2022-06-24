from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List

from .. import models, schemas
from ..database import Session, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.ResponsePostModel])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePostModel)
def create_post(post: schemas.CreatePostModel, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()

    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=schemas.ResponsePostModel)
def get_post(id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} doesn't exist'")

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post(id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.ResponsePostModel)
def update_post(id: int, post: schemas.UpdatePostModel, db: Session = Depends(get_db)):
    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_update_query.first()

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} doesn't exist'")

    post_update_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return db_post