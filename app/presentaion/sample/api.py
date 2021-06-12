from dependency_injector.wiring import Provide, inject

from flask import Blueprint, jsonify

from app.dependency import Container
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
