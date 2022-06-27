from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func

from . import oauth2
from .. import models, schemas
from ..database import Session, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.ResponsePostVotesModel])
# @router.get('/')
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)
              ):
    posts = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(
        models.Post.id
    ).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePostModel)
def create_post(post: schemas.CreatePostModel,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)
                ):

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()

    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=schemas.ResponsePostVotesModel)
def get_post(id: str, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)
             ):

    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(
        models.Post.id
    ).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} doesn't exist'")

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_post(id: str, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)
                ):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.ResponsePostModel)
def update_post(id: int, post: schemas.UpdatePostModel,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)
                ):

    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_update_query.first()

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id={id} doesn't exist'")

    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_update_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return db_post
