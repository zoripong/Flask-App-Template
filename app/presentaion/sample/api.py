import uuid

from flask import Blueprint, jsonify

api = Blueprint('sample', __name__, url_prefix='/samples')


@api.route('/', methods=['GET'])
def get_samples():
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
                'id': uuid.uuid4(),
                'name': 'name',
            }
        ],
    })
