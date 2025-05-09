# External Library imports
import os
from typing import Generator
from dotenv import load_dotenv
from contextlib import contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker


load_dotenv()

DB_USER = os.getenv('MYSQL_DB_APPLICATION_USERNAME')
DB_PASSWORD = os.getenv('MYSQL_DB_APPLICATION_PASSWORD')
DB_HOST = os.getenv('MYSQL_DB_HOST')
DB_PORT = os.getenv('MYSQL_DB_PORT')
DB_NAME = os.getenv('MYSQL_DB_NAME')

session_local = sessionmaker(autocommit=False, autoflush=False)


def get_engine() -> Engine:
    connection_string = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_string, pool_pre_ping=True)
    return engine


@contextmanager
def get_mysqldb() -> Generator[Session, None, None]:
    engine = get_engine()
    session = session_local(bind=engine)
    try:
        yield session
        session.commit()
    finally:
        session.close()