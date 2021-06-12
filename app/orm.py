from sqlalchemy.engine import Engine, create_engine as sqlalchemy_create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.session import Session as _Session, sessionmaker

Base: DeclarativeMeta = declarative_base()
Session: _Session = sessionmaker()


def create_engine(config: dict) -> Engine:
    assert config['database']['url'], "database url is required."
    return sqlalchemy_create_engine(config['database']['url'])


def create_session(config: dict) -> Session:
    return Session(bind=create_engine(config))
