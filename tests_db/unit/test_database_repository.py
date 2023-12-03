from datetime import date, datetime

import pytest

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, Game, Review, Publisher, Genre, make_review
from games.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('dave', '123456789')
    repo.add_user(user)

    user2 = repo.get_user('dave')

    assert user2 == user and user2 is user


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_game_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_articles = repo.get_number_of_games()

    # Check that the query returned 177 Articles.
    assert number_of_articles == 877


def test_repository_can_add_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_games = repo.get_number_of_games()

    new_game_id = number_of_games + 1

    game = Game(
        new_game_id,
        'new game',
    )
    repo.add_game(game)

    assert repo.get_game_by_id(new_game_id) == game


def test_repository_can_retrieve_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = repo.get_game_by_id(3010)

    # Check that the Article has the expected title.
    assert game.title == 'Xpand Rally'

    # Check that the Article is commented as expected.
    # review = [review for review in game.reviews if review.review == 'good'][0]
    #
    #
    # assert review.user.username == "xxxx"

def test_repository_does_not_retrieve_a_non_existent_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_game_by_id(1)
    assert article is None


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tags = repo.get_genres()

    assert len(tags) == 24

    tag_one = [tag for tag in tags if tag.genre_name == 'Action'][0]
    tag_two = [tag for tag in tags if tag.genre_name == 'Casual'][0]

    assert len(repo.get_games_by_genre(tag_one.genre_name)) == 380
    assert len(repo.get_games_by_genre(tag_two.genre_name)) == 366


def test_repository_returns_an_empty_list_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_game_by_id(1)

    assert articles == None


def test_repository_returns_an_empty_list_for_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article_ids = repo.get_games_by_genre('United States')

    assert len(article_ids) == 0


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('dave', '123456789')
    game = repo.get_game_by_id(3010)
    review = make_review(user, game, 5, "Awesome game")

    repo.add_review(review)

    assert review in repo.get_reviews()
    assert len(repo.get_reviews()) == 1


def test_can_add_multiple_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('dave', '123456789')
    game = repo.get_game_by_id(3010)
    review1 = make_review(user, game, 5, "Awesome game")
    review2 = make_review(user, game, 5, "Awesome game")

    repo.add_multiple_reviews([review1, review2])

    assert len(repo.get_reviews()) == 2

def test_get_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    games = repo.get_games()

    assert len(games) == 877


def test_add_multiple_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_games = repo.get_number_of_games()

    new_game_id1 = number_of_games + 1
    new_game_id2 = number_of_games + 2

    game1 = Game(
        new_game_id1,
        'new game',
    )

    game2 = Game(
        new_game_id2,
        'new game2',
    )

    repo.add_multiple_games([game1, game2])

    assert repo.get_game_by_id(new_game_id1) == game1
    assert repo.get_game_by_id(new_game_id2) == game2


def test_can_add_multiple_users(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = User('dave', '123456789')
    user2 = User('dave2', '123456789')

    repo.add_multiple_users([user1, user2])

    user1test = repo.get_user('dave')
    user2test = repo.get_user('dave2')

    assert user1 == user1test
    assert user2 == user2test


def test_get_publisher_by_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_publishers1 = repo.get_number_of_publishers() + 1

    publisher = Publisher("publisher")
    repo.add_publisher(publisher)

    number_of_publishers2 = repo.get_number_of_publishers()

    assert number_of_publishers1 == number_of_publishers2

# fix this
def test_get_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publishers = repo.get_publishers()
    assert len(publishers) == 798

# fix this
def test_get_publisher_by_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publisher = Publisher("publisher")
    repo.add_publisher(publisher)

    assert repo.get_publisher_by_name("publisher") == publisher

def test_add_multiple_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = User('dave', '123456789')
    user2 = User('dave2', '123456789')

    repo.add_multiple_users([user1, user2])

    user1test = repo.get_user('dave')
    user2test = repo.get_user('dave2')

    assert user1 == user1test
    assert user2 == user2test


def test_get_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genres = repo.get_genres()
    assert len(genres) == 24


def test_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_genres1 = len(repo.get_genres())
    genre = Genre("new_genre")
    repo.add_genre(genre)

    number_of_genres2 = len(repo.get_genres())

    assert number_of_genres1 + 1 == number_of_genres2


def test_add_multiple_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_genres1 = len(repo.get_genres())

    genre1 = Genre("new_genre")
    genre2 = Genre("new_genre2")
    repo.add_multiple_genres([genre1, genre2])

    number_of_genres2 = len(repo.get_genres())

    assert number_of_genres1 + 2 == number_of_genres2


def test_search_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = repo.search_by_title("Xpand rally")
    correct_game = [repo.get_game_by_id(3010)]

    assert game == correct_game


def test_search_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = repo.search_games_by_publisher("Techland")
    correct_game = [repo.get_game_by_id(3010)]

    assert game == correct_game


def test_search_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    game = repo.search_games_by_genre("audio production")
    correct_game = [repo.get_game_by_id(1137770)]

    assert game == correct_game