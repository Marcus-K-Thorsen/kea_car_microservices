# External Library imports
import os
from typing import Generator
from dotenv import load_dotenv
from contextlib import contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

# Internal Library imports
from src.logger_tool import logger

load_dotenv()

DB_USER = os.getenv('MYSQL_DB_APPLICATION_USERNAME')
DB_PASSWORD = os.getenv('MYSQL_DB_APPLICATION_PASSWORD')
DB_HOST = os.getenv('MYSQL_DB_HOST')
DB_PORT = os.getenv('MYSQL_DB_PORT')
DB_NAME = os.getenv('MYSQL_DB_NAME')

session_local = sessionmaker(autocommit=False, autoflush=False)


def get_engine() -> Engine:
    logger.info(f"Establishing MySQLDB connection to the database: '{DB_NAME}' on host:port '{DB_HOST}:{DB_PORT}' with the user: '{DB_USER}'...")
    connection_string = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(connection_string, pool_pre_ping=True)
    return engine


@contextmanager
def get_mysqldb() -> Generator[Session, None, None]:
    engine = get_engine()
    session = session_local(bind=engine)
    try:
        logger.info("Creating a new session")
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred: {e} rolling back the session")
        raise e
    finally:
        logger.info("Closing the session")
        session.close()