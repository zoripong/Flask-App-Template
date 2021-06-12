import uuid

from pytest import raises

from app.domain import Sample
from app.orm import Session
from app.usecases.exception import EntityNotFound
from app.usecases.sample.service import SampleService


def test_get_samples(fx_session: Session, fx_sample_service: SampleService):
    assert fx_session.query(Sample).count() == 0
    assert fx_sample_service.get_samples() == []

    samples = [Sample(name='1'), Sample(name='2')]
    fx_session.add_all(samples)
    fx_session.commit()

    assert fx_sample_service.get_samples() == samples


def test_get_sample(fx_session: Session, fx_sample_service: SampleService):
    target_id = uuid.uuid4()
    sample = Sample(id=target_id, name='sample')
    fx_session.add(sample)
    fx_session.commit()

    assert fx_sample_service.get_sample(target_id) == sample

    with raises(EntityNotFound) as e:
        fx_sample_service.get_sample(uuid.uuid4())
        assert e.class_ == Sample


def test_create_sample(fx_session: Session, fx_sample_service: SampleService):
    assert fx_session.query(Sample).count() == 0

    fx_sample_service.create_sample(name='1')
    assert fx_session.query(Sample).count() == 1
    sample = fx_session.query(Sample).filter(Sample.name == '1').one()
    assert sample is not None
