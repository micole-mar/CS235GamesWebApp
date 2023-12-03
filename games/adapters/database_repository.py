from abc import ABC
from typing import List

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from games.adapters.repository import AbstractRepository
from games.adapters.utils import search_string, title_for_sorting
from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Game_data
    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        return games

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game
    def get_game_by_id(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def get_user_by_id(self, user_id: int) -> User:
        user = None
        try:
            user = self._session_cm.session.query(
                User).filter(User._User__user_id == user_id).one()
        except NoResultFound:
            print(f'User {user_id} was not found')

        return user

    def get_games_by_genre(self, genre_name: str) -> Game:
        games = []
        try:
            games = self._session_cm.session.query(Game).filter(Game._Game__genres.any(Genre._Genre__genre_name.like(f"%{genre_name}%"))).all()
        except NoResultFound:
            print(f'Title {genre_name} was not found')
            
        return games


    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_multiple_games(self, games: List[Game]):
        with self._session_cm as scm:
            for game in games:
                scm.session.merge(game)
            scm.commit()

    def add_multiple_users(self, users: List[User]):
        with self._session_cm as scm:
            for user in users:
                scm.session.merge(user)
            scm.commit()

    def add_multiple_reviews(self, reviews: List[Review]):
        with self._session_cm as scm:
            for review in reviews:
                scm.session.merge(review)
            scm.commit()

    def get_number_of_games(self):
        total_games = self._session_cm.session.query(Game).count()
        return total_games



    # endregion

    # region Publisher data
    def get_publishers(self) -> List[Publisher]:
        publishers = self._session_cm.session.query(Publisher).order_by(Publisher._Publisher__publisher_name).all()
        return publishers

    def get_publisher_by_name(self, name: str) -> Publisher:
        publisher = None
        try:
            publisher = self._session_cm.session.query(
                Publisher).filter(Publisher._Publisher__publisher_name == name).one()
        except NoResultFound:
            print(f'Publisher {name} was not found')

        return publisher

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_multiple_publishers(self, publishers: List[Publisher]):
        with self._session_cm as scm:
            for publisher in publishers:
                scm.session.merge(publisher)
            scm.commit()

    def get_number_of_publishers(self) -> int:
        total_publishers = self._session_cm.session.query(Publisher).count()
        return total_publishers

    # endregion

    # region Genre_data
    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).order_by(Genre._Genre__genre_name).all()
        return genres

    def get_unique_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).order_by(Genre._Genre__genre_name).all()
        return genres
    #NOT SURE HOW TO SORT THIS UNIQUE GENRES MAY NOT BE IMPLEMENTED CORRECTLY IM NOT SURE 

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_multiple_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()

    # endregion

    # region Search

    def search_by_title(self, title_string: str) -> List[Game]:
        searched_games = []
        try:
            searched_games = (self._session_cm.session.query(Game).filter(Game._Game__game_title.like(f"%{title_string}%"))).all()
        except NoResultFound:
            print(f'Title {title_string} was not found')
            
        return searched_games

    def search_games_by_publisher(self, publisher_name:str) -> List[Game]:
        searched_games = []
        try:
            searched_games = self._session_cm.session.query(Game).join(Publisher).filter(Publisher._Publisher__publisher_name.like(f"%{publisher_name}%")).all()
        except NoResultFound:
            print(f'Title {publisher_name} was not found')
            
        return searched_games
    
    def search_games_by_genre(self, genre_name:str) -> List[Game]:
        searched_games = []
        try:
            searched_games = self._session_cm.session.query(Game).filter(Game._Game__genres.any(Genre._Genre__genre_name.like(f"%{genre_name}%"))).all()
        except NoResultFound:
            print(f'Title {genre_name} was not found')
            
        return searched_games

    # endregion


    # region user
    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            # user = self._session_cm.session.query(User).filter(User.username == user_name).one()
            # print(query)
            query = self._session_cm.session.query(User).filter(User._User__username == username)

            user = query.one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    # endregion

    # region reviews
    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews


    #endregion

    def add_favourite_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()


    def remove_favourite_game(self, game: Game):
        with self._session_cm as scm:
            obj = scm.session.query(Game).filter(Game._Game__game_id == game.game_id).first()
            scm.session.delete(obj)
            scm.session.commit()

    # def remove_favourite_game(self, game: Game):
    #     with self._session_cm as scm:
    #         game_id = game.game_id  # Assuming this is the game ID you want to remove.
    #
    #         # Construct an UPDATE statement to set the game_id to NULL or another appropriate value.
    #         update_query = f"UPDATE user_wishlist SET game_id = NULL WHERE game_id = {int(game_id)}"
    #
    #         # Execute the UPDATE statement.
    #         scm.session.execute(update_query)
    #         scm.commit()

    # def remove_favourite_game(self, game: Game):
    #     with self._session_cm as scm:
    #         id = int(game.game_id)
    #         delete_query = f"DELETE FROM user_wishlist WHERE game_id = {id}"
    #
    #         scm.session.execute(delete_query)
    #         scm.commit()

    # def remove_favourite_game(self, game: Game):
    #     with self._session_cm as scm:
    #         # Construct a SQL DELETE statement to remove the game from the user's wishlist.
    #         delete_query = f"DELETE FROM user_wishlist WHERE game_id = {game.game_id}"
    #
    #         try:
    #             scm.session.execute(delete_query)
    #             scm.commit()
    #         except Exception as e:
    #             # Handle any exceptions that may occur during the deletion.
    #             print(f"Error deleting game: {e}")

    # def get_wishlist(self) -> List[Game]:
    #     wishlist = self._session_cm.session.query(User.get_wishlist()).all()
    #     return wishlist

