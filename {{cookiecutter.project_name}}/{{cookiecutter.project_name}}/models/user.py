from typing import Optional

from pydantic import constr
from sqlmodel import Field, Column, SQLModel, String


class User(SQLModel, table=True):
    """
    SQLModel for the user. This is a database table.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    username: constr(strip_whitespace=True, to_lower=True) = Field(sa_column=Column("username", String, unique=True))
    admin: bool = False
