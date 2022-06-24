from sys import prefix

from fastapi import Response, status, HTTPException, Depends, APIRouter

from .. import models, schemas, utils
from ..database import Session, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUserModel)
def create_user(user: schemas.CreateUserModel, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()

    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.ResponseUserModel)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={id} doesn't exist'")

    return user
