import json
import uuid
from unittest.mock import Mock

from flask import Flask
from flask.testing import FlaskClient

from app.domain import Sample
from app.usecases.exception import EntityNotFound
from app.usecases.sample.service import SampleService


def test_get_samples(fx_wsgi_app: Flask, fx_client: FlaskClient):
    sample_service_mock = Mock(spec=SampleService)
    sample_service_mock.get_samples.return_value = [
        Sample(id=uuid.UUID(int=idx), name=str(idx))
        for idx in range(2)
    ]

    with fx_wsgi_app.container.sample_service.override(sample_service_mock):
        response = fx_client.get('/samples/')
        assert response.status_code == 200
        assert response.json == {'samples': [
            {
                'id': str(uuid.UUID(int=idx)),
                'name': str(idx),
            }
            for idx in range(2)
        ]}

    sample_service_mock.get_samples.return_value = []
    with fx_wsgi_app.container.sample_service.override(sample_service_mock):
        response = fx_client.get('/samples/')
        assert response.status_code == 200
        assert response.json == {'samples': []}


def test_get_sample(fx_wsgi_app: Flask, fx_client: FlaskClient):
    random_id = uuid.uuid4()
    mock_sample = Sample(id=random_id, name='1')

    sample_service_mock = Mock(spec=SampleService)
    sample_service_mock.get_sample.return_value = mock_sample

    with fx_wsgi_app.container.sample_service.override(sample_service_mock):
        response = fx_client.get(f'/samples/{random_id}/')
        assert response.status_code == 200
        assert response.json == {
            'sample': {
                'id': str(random_id),
                'name': '1',
            }
        }

    sample_service_mock.get_sample.side_effect = EntityNotFound(class_=Sample)
    with fx_wsgi_app.container.sample_service.override(sample_service_mock):
        response = fx_client.get(f'/samples/{random_id}/')
        assert response.status_code == 404
        data = json.loads(response.get_data(as_text=True))
        assert data == {
            'status_code': 404,
            'description': f'Cannot found sample with {random_id}',
            'message': f'Cannot found sample with {random_id}',
            'name': 'Not Found',
            'ok': False,
        }

    response = fx_client.get('/samples/INVALID_UUID/')
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert data == {
        'status_code': 400,
        'description': 'sample_id is invalid format',
        'message': 'sample_id is invalid format',
        'name': 'Bad Request',
        'ok': False,
    }


def test_create_sample(fx_wsgi_app: Flask, fx_client: FlaskClient):
    random_id = uuid.uuid4()
    mock_sample = Sample(id=random_id, name='name')

    sample_service_mock = Mock(spec=SampleService)
    sample_service_mock.create_sample.return_value = mock_sample

    with fx_wsgi_app.container.sample_service.override(sample_service_mock):
        response = fx_client.post('/samples/', json={'name': 'name'})
        assert response.status_code == 200
        assert response.json == {
            'sample': {
                'id': str(random_id),
                'name': 'name',
            }
        }

    response = fx_client.post('/samples/', json={})
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert data == {
        'status_code': 400,
        'description': 'name is required.',
        'message': 'name is required.',
        'name': 'Bad Request',
        'ok': False,
    }

    response = fx_client.post('/samples/', json={'name': ''})
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert data == {
        'status_code': 400,
        'description': 'name is required.',
        'message': 'name is required.',
        'name': 'Bad Request',
        'ok': False,
    }
