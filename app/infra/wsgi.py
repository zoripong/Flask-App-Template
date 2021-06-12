import json
import pathlib

from flask import Flask

from flask_cors import CORS


def load_configuration(path: pathlib.Path) -> dict:
    with open(path) as f:
        config = json.load(f)
    return config


def create_wsgi_app(config_path: pathlib.Path) -> Flask:
    app = Flask(__name__)

    # set configuration
    config = load_configuration(config_path)
    app.config.update(config)
    app.config['APP_CONFIG'] = config

    # set cors
    CORS(app, origins=config.get('cross_origin'))

    return app
