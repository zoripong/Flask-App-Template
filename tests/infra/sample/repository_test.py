import uuid

from app.domain.sample.model import Sample
from app.orm import Session
from app.usecases.sample.service import SampleRepository


def test_get_samples(
    fx_session: Session,
    fx_sample_repository: SampleRepository,
):
    repository = fx_sample_repository
    result = repository.get_samples()
    assert result == []

    samples = [Sample(name='1'), Sample(name='2')]
    fx_session.add_all(samples)
    fx_session.commit()

    result = repository.get_samples()
    assert result == samples


def test_find_sample(
    fx_session: Session,
    fx_sample_repository: SampleRepository,
):
    target_id = uuid.uuid4()
    sample = Sample(id=target_id, name='sample')
    fx_session.add(sample)
    fx_session.commit()

    repository = fx_sample_repository
    result = repository.find_sample(uuid.uuid4())
    assert result is None

    result = repository.find_sample(target_id)
    assert result == sample
    assert result.name == 'sample'


def test_add_sample(
    fx_session: Session,
    fx_sample_repository: SampleRepository,
):
    repository = fx_sample_repository
    assert fx_session.query(Sample).count() == 0
    repository.add_sample(Sample(name='sample'))
    fx_session.commit()
    assert fx_session.query(Sample).count() == 1
    sample = fx_session.query(Sample).filter(Sample.name == 'sample').one()
    assert sample is not None
