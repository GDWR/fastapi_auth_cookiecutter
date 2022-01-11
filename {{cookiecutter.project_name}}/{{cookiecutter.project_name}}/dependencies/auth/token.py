from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError
from sqlmodel import Session, select

from models import User
from settings import SECRET, JWT_ALGORITHM
from ..database import get_database_session


def get_user_from_token(
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
        session: Session = Depends(get_database_session)
) -> User:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token signature expired")

    jwt_username = payload.get("sub")
    if jwt_username is None:
        raise HTTPException(status_code=401, detail="Token signature expired")

    statement = select(User).where(User.username == jwt_username)
    return session.exec(statement).one()


def get_user_from_query_param(
        user_id: int,
        session: Session = Depends(get_database_session)
) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).one_or_none()
