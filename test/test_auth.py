import pytest
from flask import g, session
from project.flaskr.db import get_db


def test_register(client, app):
    # test that viewing the page renders without template errors
    assert client.get('/auth/register').status_code == 200

    # test that successful registration redirects to the login page
    response = client.post(
        '/auth/register', data={'id': 'test', 'pw': 'test', 'name' : 'a', 'phone' : 'a', 'age': 20, 'gender':'f'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    # test that the user was inserted into the database
    with app.app_context():
        assert get_db().execute(
            "select * from user_sp where id = 'test'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'name', 'phone', 'age', 'gender', 'message'), (
    ('', '', 'a','a', 10, 'a', b'Username is required.'),
    ('a', '', 'a','a', 10, 'a', b'Password is required.'),
    ('admin', 'admin' ,'a','a', 10, 'a', b'already registered'),
))
def test_register_validate_input(client, username, password, name, phone, age, gender, message):
    response = client.post(
        '/auth/register',
        data={'id': username, 'pw': password, 'phone':phone, 'name':name, 'age':age, 'gender':gender}
    )
    assert message in response.data


def test_login(client, auth):
    # test that viewing the page renders without template errors
    assert client.get('/auth/login').status_code == 200

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'admin', b'Incorrect username.'),
    ('admin', 'a', b'Incorrect password.'),
))
def test_login_validate_input(client, username, password, message):
    response = client.post(
        '/auth/login',
        data={'id': username, 'pw': password}
    )
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session