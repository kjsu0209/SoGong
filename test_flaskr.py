# content of test_flask.py
import os
import tempfile

from flask import Flask
import sqlite3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pytest
from project import app
from flaskr.db import get_db, init_db
from flaskr import auth

from flask import g, session

from flask import Blueprint

bp = Blueprint('auth', __name__)

@pytest.fixture(scope="class")
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
    app.testing = True
    app.register_blueprint(bp)

    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    with app.app_context():
        init_db()
        get_db().executescript("select Place_ID from PARKING_PLACE order by Place_ID desc")

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')
@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.mark.usefixtures("app")
def runner(app):
    return app.test_cli_runner()

def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
