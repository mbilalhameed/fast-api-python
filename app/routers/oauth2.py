from datetime import datetime, timedelta


from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .. import schemas
from .. database import get_db
from .. models import User

SECRET_KEY = "8a8aha8sh81nwd745hjj6210n12an8sbs6sjq7ja8201nsys6482bczm6"
ALGORITHM = "HS256"
ASSESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encoded = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes=ASSESS_TOKEN_EXPIRE_MINUTES)
    to_encoded.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encoded, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(access_token: str, credentials_excepton):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get('user_id')
        if user_id is None:
            raise credentials_excepton

        token_data = schemas.TokenDataModel(id=user_id)

    except JWTError as jwt_err:
        raise credentials_excepton

    return token_data


def get_current_user(access_token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_excepton = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    access_token = verify_access_token(access_token, credentials_excepton)

    current_user = db.query(User).filter(User.id == access_token.id).first()

    return current_user
