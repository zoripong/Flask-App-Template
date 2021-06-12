from typing import List

from app.domain.sample.model import Sample
from app.infra.context import session
from app.usecases.sample.service import SampleRepository


class SQLAlchemySampleRepository(SampleRepository):
    def get_samples(self) -> List[Sample]:
        return session.query(Sample).all()
