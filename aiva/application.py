"""
application.py
- creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_cors import CORS
from tensorflow import keras
from os import path


def create_app(app_name='AIVA_API'):
    app = Flask(app_name)
    app.config.from_object('aiva.config.BaseConfig')
    app.config['JSON_AS_ASCII'] = False

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    from aiva.api import api
    app.register_blueprint(api, url_prefix="/api")

    return app
