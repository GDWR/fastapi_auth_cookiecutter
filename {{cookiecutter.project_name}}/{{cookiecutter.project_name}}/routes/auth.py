from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlmodel import Session, select

from dependencies.database import get_database_session
from models import User, Password
from settings import JWT_DURATION_MINUTES, JWT_ALGORITHM, SECRET
from utils.password import validate_password

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(
        form: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_database_session)
):
    statement = select(User, Password).join(Password).where(User.username == form.username)
    user, password = session.exec(statement).one()

    if not validate_password(form.password + password.salt, password.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    current_time = datetime.utcnow()
    token_data = {
        "sub": user.username,
        "exp": current_time + timedelta(minutes=JWT_DURATION_MINUTES),
        "iat": current_time,
    }
    token = jwt.encode(token_data, SECRET, algorithm=JWT_ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
