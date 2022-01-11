from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from dependencies.auth.token import get_user_from_token, get_user_from_query_param
from models import User

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/", response_model=User)
async def get_user_information(user: User = Depends(get_user_from_token)) -> User:
    """Get user information using the context of a token."""
    return user


@router.get("/{user_id}", response_model=User)
async def get_user_information(user: Optional[User] = Depends(get_user_from_query_param)) -> User:
    """Get user information from provide user_id."""
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
