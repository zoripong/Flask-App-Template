import json
import pathlib

from flask import Flask

from flask_cors import CORS

from app.dependency import Container
from app.presentaion.sample import api as sample_api_module
from app.presentaion.sample.api import api as sample_api


def load_dependency_injection_configuration() -> Container:
    container = Container()
    container.wire(modules=[sample_api_module])
    return container


def load_configuration(path: pathlib.Path) -> dict:
    with open(path) as f:
        config = json.load(f)
    return config


def create_wsgi_app(config_path: pathlib.Path) -> Flask:
    app = Flask(__name__)

    # set di configuration
    app.container = load_dependency_injection_configuration()

    # set configuration
    config = load_configuration(config_path)
    app.config.update(config)
    app.config['APP_CONFIG'] = config

    # set cors
    CORS(app, origins=config.get('cross_origin'))

    # set blueprint
    app.register_blueprint(sample_api)

    return app
