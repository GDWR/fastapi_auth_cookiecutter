import time

from sqlalchemy.exc import OperationalError, IntegrityError
from sqlmodel import Session, SQLModel, create_engine as sqlmodel_create_engine

from models import User, Password
from settings import DATABASE_PASSWORD
from utils.password import hash_password, generate_salt


def create_engine(attempts: int, wait_time_s: float = 2.5):
    """
    When the database is created and at the same time
        via docker-compose. The data might not connect straight away.
        
    :param attempts: How many times to attempt to connect to the database.
    :param wait_time_s: How long to wait after each attempt, in seconds.
    :raises OperationalError: When unable to connect to the database after the 
        specified attempts.
    """""
    connection_string = f"postgresql://postgres:{DATABASE_PASSWORD}@database/postgres"
    for attempt in range(1, attempts + 1):
        try:
            return sqlmodel_create_engine(connection_string)
        except OperationalError:
            if attempt == attempts:
                raise
            time.sleep(wait_time_s)


engine = create_engine(attempts=10)


def create_db_and_tables() -> None:
    """Create the tables in the database from the SQLModels"""
    SQLModel.metadata.create_all(engine)


def create_admin() -> None:
    """
    Create the admin account.
        If the account already exists, nothing will happen.
    """
    with Session(engine) as session:
        admin = User(id=0, username="admin", admin=True)
        session.add(admin)

        salt = generate_salt()
        password = Password(user_id=admin.id, password=hash_password("admin" + salt), salt=salt)
        session.add(password)

        try:
            session.commit()
        except IntegrityError:
            ...  # The account already exists
