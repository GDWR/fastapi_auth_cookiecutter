from sqlmodel import Session

from database import engine


def get_database_session() -> Session:
    with Session(engine) as session:
        yield session
