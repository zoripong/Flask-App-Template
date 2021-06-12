from flask import Flask
from flask.testing import FlaskClient

from ormeasy.sqlalchemy import test_connection

from pytest import fixture

from sqlalchemy.engine import Connection, Engine

from app import context
from app.infra.sample.repository import SQLAlchemySampleRepository
from app.infra.wsgi import create_wsgi_app
from app.orm import (
    Base,
    Session,
    create_engine,
    create_session,
    import_all_modules,
)
from app.usecases.sample.service import SampleRepository, SampleService


@fixture
def fx_config_data() -> dict:
    return {
        'debug': False,
        'cross_origin': [],
        'database': {
            'url': 'postgresql://localhost:5432/flask-template-test',
        }
    }


@fixture
def fx_config(request, fx_config_data: dict) -> dict:
    prev_app = context._test_app
    prev_ctx = context._test_ctx

    context._test_app = fx_config_data
    context._test_ctx = request
    yield fx_config_data

    context._test_app = prev_app
    context._test_ctx = prev_ctx


@fixture
def fx_wsgi_app(fx_config: dict) -> Flask:
    return create_wsgi_app(fx_config)


@fixture
def fx_client(fx_wsgi_app: Flask) -> FlaskClient:
    with fx_wsgi_app.test_client() as client:
        yield client


@fixture
def fx_database_engine(fx_config: dict) -> Engine:
    return create_engine(fx_config)


@fixture
def fx_database_connection(fx_database_engine: Engine) -> Connection:
    engine = fx_database_engine
    metadata = Base.metadata
    import_all_modules()
    metadata.create_all(engine)
    try:
        with test_connection(fx_config, metadata, engine, False) as conn:
            yield conn
    finally:
        metadata.drop_all(engine, checkfirst=True)


@fixture
def fx_session(
    fx_config: dict,
    fx_database_connection: Connection,
) -> Session:
    session = create_session(fx_database_connection)
    try:
        context._test_ctx._current_session = session
        yield session
    finally:
        session.close()
        context._test_ctx._current_session = None


@fixture
def fx_sample_repository() -> SampleRepository:
    return SQLAlchemySampleRepository()


@fixture
def fx_sample_service(fx_sample_repository: SampleRepository) -> SampleService:
    return SampleService(repository=fx_sample_repository)
