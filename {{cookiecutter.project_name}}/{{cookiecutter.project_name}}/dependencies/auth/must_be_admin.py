from fastapi import Depends, HTTPException

from models import User
from .token import get_user_from_token


def must_be_admin(user: User = Depends(get_user_from_token)) -> None:
    if not user.admin:
        raise HTTPException(status_code=403, detail="Forbidden")
