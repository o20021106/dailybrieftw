import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .bp import bp
from dailybrieftw.utils.database import db_session, init_db


def create_app():
    app = Flask(__name__)
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    init_db()
    with app.app_context():
        app.register_blueprint(bp)
    return app
