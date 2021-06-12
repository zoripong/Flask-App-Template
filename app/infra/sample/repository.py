import typing as t
import uuid

from app.domain.sample.model import Sample
from app.infra.context import session
from app.usecases.sample.service import SampleRepository


class SQLAlchemySampleRepository(SampleRepository):
    def get_samples(self) -> t.List[Sample]:
        return session.query(Sample).all()

    def find_sample(self, sample_id: uuid.UUID) -> t.Optional[Sample]:
        return session.query(Sample).get(sample_id)
