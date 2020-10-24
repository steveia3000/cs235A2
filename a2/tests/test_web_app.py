import pytest
from flask import session


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    response = client.post(
        '/authentication/register',
        data={'username': 'evefeng', 'password': 'Feng2000'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('a', '', b'Your username is too short'),
        ('abcdefg', '', b'Your password is required'),
        ('abcdefg', '123', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit')))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'


    with client:
        client.get('/')
        assert session['username'] == 'mjackson'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235 Assignment 2' in response.data


def test_login_required_to_comment(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_comment(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/review?movie=2')

    response = client.post(
        '/review',
        data={'review': 'Who needs quarantine?', 'movie_id': 2}
    )
    assert response.headers['Location'] == 'http://localhost/movies_by_date?date=2012&view_reviews_for=2'


@pytest.mark.parametrize(('comment', 'messages'), (
        ('Who thinks Trump is a fuckwit?', (b'Your review must not contain profanity')),
        ('H', (b'Your review is too short')),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_comment_with_invalid_input(client, auth, comment, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an movie.
    response = client.post(
        '/review',
        data={'review': comment, 'movie_id': 2}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movies_without_date(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_date')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first movie.
    assert b'2012' in response.data
    assert b'Guardians of the Galaxy' in response.data


def test_movies_with_date(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_date?date=2012')
    assert response.status_code == 200

    assert b'2012' in response.data


def test_movies_with_comment(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_date?date=2012&view_reviews_for=2')
    assert response.status_code == 200

    # Check that all comments for specified movie are included on the page.
    assert b'Yeah Freddie, bad news' in response.data

def test_movies_with_tag(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Comedy')
    assert response.status_code == 200

    # Check that all movies tagged with 'Health' are included on the page.
    assert b'Sing' in response.data
