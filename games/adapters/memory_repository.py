import csv
import os
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from games.adapters.repository import AbstractRepository, RepositoryException
from games.domainmodel.model import Game, Genre, User, Review, make_review
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__reviews = list()
        self.__users = list()
        self.__wishlists = list()
        self.__publishers = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username), None)

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)

    def add_genre(self, genre: Genre):
        if genre in self.__genres:
            return
        insort_left(self.__genres, genre)

    def get_games(self) -> List[Game]:
        return sorted(self.__games, key=lambda game: game.title)
    
    def get_number_of_games(self):
        return len(self.__games)
    
    def get_game(self, game_id: int) -> Game:
        return next((game for game in self.__games if game.game_id == game_id), None)
    
    def get_game_by_id(self, game_id):
        for game in self.__games:
            if game.game_id == game_id:
                return game

    def search_by_title(self, title: str):
        title = title.lower()
        return [game for game in self.__games if title in game.title.lower()]

    def search_games_by_publisher(self, publisher_name: str) -> List[Game]:
        publisher_name = publisher_name.lower()
        return [game for game in self.__games if
                game.publisher is not None and publisher_name in str(game.publisher).lower()]

    def search_games_by_genre(self, genre_name: str) -> List[Game]:
        genre_name = genre_name.lower()
        return [game for game in self.__games if any(genre_name in str(genre).lower() for genre in game.genres)]

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def get_publishers(self):
        return self.__publishers

    def get_reviews_for_game(self, game_id):
        return [review for review in self.__reviews]

    def get_unique_genres(self):
        return sorted(self.__genres)  # Return sorted list of unique genres

    def get_games_by_genre(self, genre_name: str):
        result = list()
        genre_name = genre_name.lower()
        for game in self.__games:
            for genre in game.genres:
                if str('genre '+ genre_name) == str(genre).strip('<>').lower():
                    result.append(game)
        return result

    # def get_wishlist(self, user: User):
    #     return
    def add_favourite_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__wishlists, game)

    def remove_favourite_game(self, game: Game):
        if isinstance(game, Game):
            self.__wishlists.remove(game)

    def get_favourite_game(self, user: User, game_id: int) -> Game:
        for game in self.__wishlists:
            if game.game_id == game_id:
                return game
        return None


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(csv_filename: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(csv_filename):
        user = User(
            username=data_row[1],
            password=data_row[2]
        )
        repo.add_user(user)
        users[data_row[0]] = user

    # Save the updated user data back to the CSV file
    with open(csv_filename, mode='w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow(['user_id', 'username', 'password'])
        # Write user data
        for user_id, user in users.items():
            writer.writerow([user_id, user.username, user.password])
    return users


# def load_reviews(data_path: Path, repo: MemoryRepository, users):
#     reviews_filename = str(Path(data_path) / "reviews.csv")
#     for data_row in read_csv_file(reviews_filename):
#         comment = make_review(
#             review_text=data_row[3],
#             user=users[data_row[1]],
#             game=repo.get_game(int(data_row[2])),
#             timestamp=datetime.fromisoformat(data_row[4])
#         )
#         repo.add_review(comment)

    
def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")

    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()
    games = reader.dataset_of_games

    # Add games to the repo, and let the MemoryRepository handle genre extraction
    for game in games:
        repo.add_game(game)
        for genre in game.genres:
            repo.add_genre(genre)
        #for language in game.languages:
           # game.add_language(language)

    # Now you can use the get_unique_genres method to get the list of genres
    # genres_list = repo.get_unique_genres()


# def populate(repo: AbstractRepository):
#     dir_name = os.path.dirname(os.path.abspath(__file__))
#     games_file_name = os.path.join(dir_name, "data/games.csv")
#     reader = GameFileCSVReader(games_file_name)
#     reader.read_csv_file()
#     games = reader.dataset_of_games
#     # Add games to the repo
#     for game in games:
#         repo.add_game(game)



