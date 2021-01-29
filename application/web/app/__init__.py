import os

from flask import Flask

from .bp import bp


def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.register_blueprint(bp)
    return app
