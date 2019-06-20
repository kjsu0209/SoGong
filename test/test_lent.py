import pytest
from flask import g, session
from project.flaskr.db import get_db


def test_add_place(client, auth, app):
    # test that viewing the page renders without template errors
    auth.login()
    with client:
        client.get('/')
        assert session['user_id'] == 'test'

    assert client.get('/owner/').status_code == 200
    # test that successful registration redirects to the login page
    response = client.post(
        '/owner/add_place', data={'id': 'test', 'adr':'test', 'price': 3000}
    )
    assert 'http://localhost/owner' == response.headers['Location']

    # test that the parking place was inserted into the database
    with app.app_context():
        assert get_db().execute(
            "select * from parking_place where owner_id = 'test' and Adr='test",
        ).fetchone() is not None