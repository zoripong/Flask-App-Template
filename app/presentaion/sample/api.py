import uuid

from dependency_injector.wiring import Provide, inject

from flask import Blueprint, jsonify

from app.dependency import Container
from app.presentaion.exception import BadRequest, NotFound
from app.usecases.exception import EntityNotFound
from app.usecases.sample.service import SampleService

api = Blueprint('sample', __name__, url_prefix='/samples')


@api.route('/', methods=['GET'])
@inject
def get_samples(
    sample_service: SampleService = Provide[Container.sample_service],
):
    """List of Sample

    .. code-block:: http

       GET /samples/ HTTP/1.1

    .. code-block:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
           "samples": [
                {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "name": "name"
                },
                {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "name": "name"
                }
           ]
       }

    """

    return jsonify({
        'samples': [
            {
                'id': service.id,
                'name': service.name,
            } for service in sample_service.get_samples()
        ],
    })


@api.route('/<sample_id>/', methods=['GET'])
@inject
def get_sample(
    sample_id: str,
    sample_service: SampleService = Provide[Container.sample_service],
):
    """Specific Sample

    .. code-block:: http

       GET /samples/00000000-0000-0000-0000-000000000000/ HTTP/1.1

    .. code-block:: http

       HTTP/1.1 200 OK
       Content-Type: application/json

       {
           "sample": {
                "id": "00000000-0000-0000-0000-000000000000",
                "name": "name"
            }
       }

    """
    try:
        parsed_sample_id = uuid.UUID(sample_id)
    except ValueError:
        raise BadRequest('sample_id is invalid format')
    try:
        sample = sample_service.get_sample(sample_id=parsed_sample_id)
    except EntityNotFound:
        raise NotFound(f'Cannot found sample with {sample_id}')
    return jsonify({
        'sample': {
            'id': sample.id,
            'name': sample.name,
        },
    })
