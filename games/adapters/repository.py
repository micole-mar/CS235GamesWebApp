import abc
from typing import List
from datetime import date

from games.domainmodel.model import Game, User, Review

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        """Adds game to list of games """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """Gives list of games """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_title(self, title: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_unique_genres(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self, game_id):
        """Retrieves a game by its unique ID """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id):
        """Retrieves a game by its unique ID """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If the Review doesn't have bidirectional links with a Game and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.game is None or review not in review.game.reviews:
            raise RepositoryException('Review not correctly attached to a Game')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_favourite_game(self, game: Game):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite_game(self, game: Game):
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_wishlist(self) -> List[Game]:
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError