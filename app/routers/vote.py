from fastapi import Response, status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas
from ..database import Session, get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(curr_vote: schemas.VoteModel, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == curr_vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {curr_vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == curr_vote.post_id,
        models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if curr_vote.dir == 1:
        if found_vote is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already voted on this post")

        new_vote = models.Vote(post_id=curr_vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {
            "message": "Successfully added vote"
        }

    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not voted on this post")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {
            "message": "Successfully deleted vote"
        }
