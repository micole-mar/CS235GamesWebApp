import pytest
import os
from games.adapters.memory_repository import MemoryRepository
from games.gameDescription import services as games_services
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.browse import services as browse_services
from games.genres import services as genres_services
from games.search import services as search_services
from games.gameDescription import services as game_services
from games.authentication import services as authentication_services
from games.profile import services as profile_services

# Create a fixture to provide a pre-populated repository to each test function
@pytest.fixture
def populated_repo():
    repo = MemoryRepository()
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join("games/adapters/data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)
        for genre in game.genres:
            repo.add_genre(genre)
    return repo

# Testing that I can get a game through its id.
def test_get_game_by_id(populated_repo):
    game = games_services.get_game_by_id(populated_repo, 1228870)
    assert game is not None
    assert game.title == "Bartlow's Dread Machine"

# Testing that the service layer retrieves the correct number of game objects.
def test_get_number_of_games(populated_repo):
    num_games = games_services.get_number_of_games(populated_repo)
    assert num_games == 877

# Testing that only a certain number of games are returned for pagination.
def test_pagination(populated_repo):
    page = browse_services.get_games_for_page(0, 10, populated_repo)
    assert len(page) == 10

# Testing that the correct games are shown when browsing the genres.
def test_get_games_by_genre(populated_repo):
    games = genres_services.get_games_by_genre(populated_repo, "Gore")
    assert games is not None
    assert str(games) == ("[<Game 648070, CrisisActionVR>, <Game 854190, Russian Gangsta In HELL>]")

# Testing that the search bar in task 5 works when searching by title and returns the correct info.
def test_search_by_type(populated_repo):
    games = search_services.search_by_type(populated_repo, "rally", 'title')
    assert games is not None
    assert str(games) == "[<Game 3010, Xpand Rally>]"

# Testing that the search bar in task 5 works when searching by genre and returns the correct info.
def test_search_by_genre(populated_repo):
    games = search_services.search_by_type(populated_repo, "gore", 'genre')
    assert games is not None
    assert str(games) == "[<Game 648070, CrisisActionVR>, <Game 854190, Russian Gangsta In HELL>]"

# Testing that the search bar in task 5 works when searching by publisher and returns the correct info.
def test_search_by_publisher(populated_repo):
    games = search_services.search_by_type(populated_repo, "curve", 'publisher')
    assert games is not None
    assert str(games) == "[<Game 435790, 10 Second Ninja X>]"

# Testing that the list of correct unique genres are being returned.
def test_get_unique_genres(populated_repo):
    genres = genres_services.get_unique_genres(populated_repo)
    assert str(genres) == "[<Genre Action>, <Genre Adventure>, <Genre Animation & Modeling>, <Genre Audio Production>, <Genre Casual>, <Genre Design & Illustration>, <Genre Early Access>, <Genre Education>, <Genre Free to Play>, <Genre Game Development>, <Genre Gore>, <Genre Indie>, <Genre Massively Multiplayer>, <Genre Photo Editing>, <Genre RPG>, <Genre Racing>, <Genre Simulation>, <Genre Software Training>, <Genre Sports>, <Genre Strategy>, <Genre Utilities>, <Genre Video Production>, <Genre Violent>, <Genre Web Publishing>]"

# Testing that the correct list of games is retrieved for a particular page. I have only tested the first game because it will be too long otherwise.
def test_get_games_for_page(populated_repo):
    games = browse_services.get_games_for_page(0, 10, populated_repo)
    assert str(games[0]) == "{'game_id': 435790, 'title': '10 Second Ninja X', 'game_url': 'Jul 19, 2016', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/435790/header.jpg?t=1634742090', 'genres': '  Action, Indie,', 'publisher': 'Curve Games', 'price': 0.99}"

# Testing that the get_games function works and it can get games from games.csv. I am only testing that the first game matches because it'll be too long otherwise.
def test_get_games(populated_repo):
    games = browse_services.get_games_for_page(0, 10, populated_repo)
    assert str(games[0]) == "{'game_id': 435790, 'title': '10 Second Ninja X', 'game_url': 'Jul 19, 2016', 'image_url': 'https://cdn.akamai.steamstatic.com/steam/apps/435790/header.jpg?t=1634742090', 'genres': '  Action, Indie,', 'publisher': 'Curve Games', 'price': 0.99}"

# Testing that the add_user and get_user functions work and they can add a user and get a user from the repo.
def test_can_add_user(populated_repo):
    new_username = "jz"
    new_password = "abcd1A23"

    authentication_services.add_user(new_username, new_password, populated_repo)

    user_as_dict = authentication_services.get_user(new_username, populated_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')

# Testing that if a user enters a username that already exists, the NameNotUniqueException is raised.
def test_cannot_add_user_with_existing_name(populated_repo):
    username = 'xxx'
    password = 'abcd1A23'

    authentication_services.add_user(username, password, populated_repo)

    new_username = 'xxx'
    new_password = 'abcd1A23'

    with pytest.raises(authentication_services.NameNotUniqueException):
        authentication_services.add_user(new_username, new_password, populated_repo)

# Testing that the authenticate_user function works, and if the authentication fails, the AuthenticationException is raised.
def test_authentication_with_valid_credentials(populated_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    authentication_services.add_user(new_user_name, new_password, populated_repo)

    try:
        authentication_services.authenticate_user(new_user_name, new_password, populated_repo)
    except authentication_services.AuthenticationException:
        assert False

# Testing that if the user tried to sign in with invalid credentials (i.e. wrong password), the AuthenticationException is raised.
def test_authentication_with_invalid_credentials(populated_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    authentication_services.add_user(new_user_name, new_password, populated_repo)

    with pytest.raises(authentication_services.AuthenticationException):
        authentication_services.authenticate_user(new_user_name, '0987654321', populated_repo)

# Testing if a user can add a review (get_reviews_for_game)
def test_can_add_review(populated_repo):
    game_id = 7940
    comment_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'fmercury'
    rating = 5
    password = "Password123"
    # Call the service layer to add the comment.
    authentication_services.add_user(user_name, password, populated_repo)
    games_services.add_review(game_id, comment_text, user_name, rating, populated_repo)

    # Retrieve the comments for the article from the repository.
    comments_as_dict = games_services.get_reviews_for_game(game_id, populated_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['review_text'] for dictionary in comments_as_dict if dictionary['review_text'] == comment_text),
        None) is not None

# Testing that game that doesn't exist cannot be called (get_game).
def test_cannot_get_game_with_non_existent_id(populated_repo):
    article_id = 7

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(games_services.NonExistentGameException):
        games_services.get_game(article_id, populated_repo)

# Testing that a review cannot be added for a non existent game.
def test_cannot_add_comment_for_non_existent_article(populated_repo):
    game_id = 1
    comment_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'fmercury'
    rating = 5
    password = "Password123"
    # Call the service layer to add the comment.

    # Call the service layer to attempt to add the comment.
    with pytest.raises(games_services.NonExistentGameException):
        games_services.add_review(game_id, comment_text, user_name, rating, populated_repo)


# Testing
def test_cannot_add_comment_by_unknown_user(populated_repo):
    game_id = 1
    comment_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'fmercury'
    rating = 5
    password = "Password123"
    # Call the service layer to add the comment.

    # Call the service layer to attempt to add the comment.
    with pytest.raises(games_services.UnknownUserException):
        games_services.add_review(game_id, comment_text, user_name, rating, populated_repo)