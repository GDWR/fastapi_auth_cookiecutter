from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Password(SQLModel, table=True):
    """
    SQLModel for the password.
        This is a database table.

    This is done on another table as it should only
        be accessed in very specific cases. Whereas the
        User will be accessed alot without needing this
        sensitive information.
    """
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    user: "User" = Relationship()

    password: str
    salt: str
