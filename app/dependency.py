from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from app.infra.sample.repository import SQLAlchemySampleRepository
from app.usecases.sample.service import SampleService


class Container(DeclarativeContainer):
    sample_repository = Factory(SQLAlchemySampleRepository)
    sample_service = Factory(SampleService, repository=sample_repository)
