import abc
import typing as t
import uuid

from app.context import session
from app.domain.sample.model import Sample
from app.usecases.exception import EntityNotFound


class SampleRepository(abc.ABC):

    @abc.abstractmethod
    def get_samples(self) -> t.List[Sample]:
        """samples 리스트를 조회해옵니다."""
        ...

    @abc.abstractmethod
    def find_sample(self, sample_id: uuid.UUID) -> t.Optional[Sample]:
        """id 를 통해 sample 을 조회해옵니다."""
        ...

    @abc.abstractmethod
    def add_sample(self, sample: Sample):
        """sample을 생성합니다."""
        ...


class SampleService:
    def __init__(self, repository: SampleRepository):
        self._repository = repository

    def get_samples(self) -> t.List[Sample]:
        return self._repository.get_samples()

    def get_sample(self, sample_id: uuid.UUID) -> Sample:
        sample = self._repository.find_sample(sample_id)
        if not sample:
            raise EntityNotFound(class_=Sample)
        return sample

    def create_sample(self, name: str) -> Sample:
        sample = Sample(name=name)
        self._repository.add_sample(sample)
        session.commit()
        return sample
