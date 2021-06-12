from sqlalchemy.engine import Engine, create_engine as sqlalchemy_create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.session import Session as _Session, sessionmaker

from werkzeug.utils import find_modules, import_string

Base: DeclarativeMeta = declarative_base()
Session: _Session = sessionmaker()
ENTITY_ROOT_PATH = 'app.domain'


def import_all_modules():
    for name in find_modules(ENTITY_ROOT_PATH, include_packages=True):
        import_string(name)


def create_engine(config: dict) -> Engine:
    assert config['database']['url'], "database url is required."
    db_options = config.get('database', {}).copy()
    db_options.pop('url', None)
    return sqlalchemy_create_engine(config['database']['url'], **db_options)


def create_session(bind: Engine) -> Session:
    return Session(bind=bind)
