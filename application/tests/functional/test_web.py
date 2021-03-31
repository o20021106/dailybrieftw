from datetime import datetime
import sys
import os
sys.path.append(os.getcwd())

import pytest

from web.app import create_app


app = create_app()

@pytest.fixture()
def client():
    flask_app = create_app()
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_brief(client):
    response = client.get('/brief')
    assert response.status_code == 200
    assert b'audio_url' in response.data
    assert b'articles' in response.data