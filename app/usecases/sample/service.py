import abc
from typing import List

from app.domain import Sample


class SampleRepository(abc.ABC):

    @abc.abstractmethod
    def get_samples(self) -> List[Sample]:
        """samples 리스트를 조회해옵니다."""
        ...


class SampleService:
    def __init__(self, repository: SampleRepository):
        self._repository = repository

    def get_samples(self) -> List[Sample]:
        return self._repository.get_samples()
