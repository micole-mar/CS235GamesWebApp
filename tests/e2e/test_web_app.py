import pytest

from flask import session


def test_register(client):
    # we retrieve the register page
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200  # check if retrieved

    # Check we can successfully register a user, using a valid username and password
    response = client.post(
        '/authentication/register',
        data={'username': 'bob123', 'password': 'P@ssword123'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Your user name is required'), # passed
    ('aa', '', b'Your user name is too short'), # passed
    ('test', '', b'Your password is required'), # passed
    ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
           a lower case letter and a digit'), # passed
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_register_with_existing_username(client):
    # Register a user with a specific username.
    response = client.post(
        '/authentication/register',
        data={'username': 'bob123', 'password': 'P@ssword123'}
    )
    assert response.headers['Location'] == '/authentication/login'

    # Attempt to register another user with the same username.
    response = client.post(
        '/authentication/register',
        data={'username': 'bob123', 'password': 'AnotherPassword123'}
    )

    # Check if the response contains an error message indicating that the username is already taken.
    assert b'Your username is already taken - please supply another' in response.data


def test_login(client, auth):
    # we retrieve the register page
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200  # check if retrieved

    # Check we can successfully register a user, using a valid username and password
    response = client.post(
        '/authentication/register',
        data={'username': 'bob123', 'password': 'P@ssword123'}
    )

    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = client.post(
        '/authentication/login',
        data={'username': 'bob123', 'password': 'P@ssword123'}
    )
    print(response.headers['Location'])
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'bob123'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'id' not in session


def test_login_required_to_review(client):
    response = client.post('/review/7940')
    assert response.headers['Location'] == '/authentication/login'


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b"Game Library" in response.data


def test_games_with_genre(client):
    # Check that we can retrieve the games page.
    response = client.get('/genre/Photo%20Editing')
    assert response.status_code == 200

    # Check that all games with genre 'Photo Editing' are included on the page.
    assert b'Photo Editing Games' in response.data


def test_review_too_short(client, auth):
    # Login a user.
    auth.login()

    # Attempt to submit a comment that is too short.
    response = client.post(
        '/review/7940',
        data={'review': 'Hi', 'game_id': 7940}
    )

    # Check that the response redirects to target URL.
    assert b'You should be redirected automatically to the target URL' in response.data


def test_review_contains_profanity(client, auth):
    # Login a user.
    auth.login()

    # Attempt to submit a comment that contains profanity.
    response = client.post(
        '/review/7940',
        data={'review': 'This game is awful f***ing sh*t!', 'game_id': 7940}
    )

    # Check that the response redirects to target URL.
    assert b'You should be redirected automatically to the target URL' in response.data


def test_review_too_short_and_contains_profanity(client, auth):
    # Login a user.
    auth.login()

    # Attempt to submit a comment that is both too short and contains profanity.
    response = client.post(
        '/review/7940',
        data={'review': 'A**', 'game_id': 7940}
    )

    # Check that the response redirects to target URL.
    assert b'You should be redirected automatically to the target URL' in response.data


def test_invalid_review_rating(client, auth):
    auth.login()
    # Attempt to submit a review with an invalid rating (e.g., 0).
    response = client.post(
        '/review/7940',
        data={'review': 'This is a test review.', 'rating': '0', 'game_id': 7940}
    )
    # Check that the response redirects to the target URL.
    assert b'You should be redirected automatically to the target URL' in response.data
    # Attempt to submit a review with an invalid rating (e.g., 6).
    response = client.post(
        '/review/7940',
        data={'review': 'This is another test review.', 'rating': '6', 'game_id': 7940}
    )
    # Check that the response redirects to the target URL.
    assert b'You should be redirected automatically to the target URL' in response.data


