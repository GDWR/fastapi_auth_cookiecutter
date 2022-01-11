from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import select, Session

from dependencies.auth import must_be_admin
from dependencies.database import get_database_session
from models import User, Password
from models.user_form import UserForm
from utils.password import hash_password, generate_salt

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(must_be_admin)]
)


@router.post("/user", response_model=User)
def add_user(user_form: UserForm, session: Session = Depends(get_database_session)) -> User:
    new_user = User(username=user_form.username, admin=user_form.admin)
    session.add(new_user)

    salt = generate_salt()
    password = Password(password=hash_password(user_form.password + salt), salt=salt)

    password.user = new_user
    session.add(password)

    try:
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username already exists")


@router.delete("/user")
def delete_user(user_id: int, session: Session = Depends(get_database_session)) -> None:
    statement = select(User, Password).join(Password).where(User.id == user_id)
    try:
        user, password = session.exec(statement).one()
        session.delete(user)
        session.delete(password)
        session.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/user", response_model=User)
def update_user(user_id: int, user_form: UserForm, session: Session = Depends(get_database_session)) -> User:
    statement = select(User, Password).join(Password).where(User.id == user_id)
    try:
        user, password = session.exec(statement).one()
        user.username = user_form.username
        user.admin = user_form.admin
        password.password = hash_password(user_form.password)
        session.commit()
        return user
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
