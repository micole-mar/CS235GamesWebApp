import csv
import os

from games.domainmodel.model import Genre, Game, Publisher, User, Review

import games.adapters.database_repository as dbrepo

from games.adapters.database_repository import SqlAlchemyRepository



class GameFileCSVReader:
    def __init__(self, filename):
        self.__filename = filename
        self.__dataset_of_games = []
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()

        self.__game_reviews = {}


    def read_csv_file(self):
        if not os.path.exists(self.__filename):
            print(f"path {self.__filename} does not exist!")
            return
        with open(self.__filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    game_id = int(row["AppID"])
                    title = row["Name"]
                    game = Game(game_id, title)
                    game.release_date = row["Release date"]
                    game.price = float(row["Price"])
                    game.description = row["About the game"]

                    game.image_url = row["Header image"]

                    # game.screenshots = row["Screenshots"].split(",")
                    game.screenshots = row["Screenshots"]

                    game.website_url = row["Website"]
                    # languages = row["Supported languages"].split(",")
                    game.languages = row["Supported languages"]
                    game.windows = row["Windows"].lower() == "true"
                    game.mac = row["Mac"].lower() == "true"
                    game.linux = row.get("Linux", "").lower() == "true"

                    publisher = Publisher(row["Publishers"])
                    self.__dataset_of_publishers.add(publisher)
                    game.publisher = publisher

                    # developer_names = row.get("Developers", "").split(",")
                    # developers = [developer.strip() for developer in developer_names]
                    # game.developers = developers
                    game.developers = row["Developers"]

                    # player_modes = row.get("Categories", "").split(",")
                    game.player_modes = row["Categories"]

                    recommendations = int(row.get("Recommendations", "0"))
                    game.recommendations = recommendations

                    genre_names = row["Genres"].split(",")
                    for genre_name in genre_names:
                        genre = Genre(genre_name.strip())
                        self.__dataset_of_genres.add(genre)
                        game.add_genre(genre)

                    # self.__game_reviews[game_id] = game

                    self.__dataset_of_games.append(game)

                    movie_url = row.get("Movies")
                    if movie_url:
                        game.movie_url = movie_url

                except ValueError as e:
                    print(f"Skipping row due to invalid data: {e}")
                except KeyError as e:
                    print(f"Skipping row due to missing key: {e}")

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_genres_count(self):
        return len(self.__dataset_of_genres)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres


# class UserFileCSVReader:
#     def __init__(self, filename):
#         self.__filename = filename
#         self.__dataset_of_users = []
#
#     def read_csv_file(self):
#         if not os.path.exists(self.__filename):
#             print(f"path {self.__filename} does not exist!")
#             return
#         with open(self.__filename, 'r', encoding='utf-8-sig') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 try:
#                     user_id = int(row["user_id"])
#                     username = str(row["username"])
#                     password = str(row["password"])
#
#                     user = User(username,password)
#
#                     self.__dataset_of_users.append(user)
#
#                 except ValueError as e:
#                     print(f"Skipping row due to invalid data: {e}")
#                 except KeyError as e:
#                     print(f"Skipping row due to missing key: {e}")
#
#     def get_unique_users_count(self):
#         return len(self.__dataset_of_users)
#
#     @property
#     def dataset_of_users(self) -> list:
#         return self.__dataset_of_users


# class ReviewFileCSVReader:
#     def __init__(self, filename):
#         self.__filename = filename
#         self.__dataset_of_reviews = []
#         # self.sql_repository = SqlAlchemyRepository(session_factory)  # Replace 'session_factory' with your session factory.
#
#     def read_csv_file(self):
#         if not os.path.exists(self.__filename):
#             print(f"path {self.__filename} does not exist!")
#             return
#         with open(self.__filename, 'r', encoding='utf-8-sig') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 try:
#                     review_id = int(row["review_id"])
#                     game_id = int(row["game_id"])
#                     user_id = int(row["user_id"])
#                     review_text = str(row["review_text"])
#                     rating = int(row["rating"])
#
#                     print('print test: ', game_id, user_id)
#
#                     game = SqlAlchemyRepository.get_game_by_id(game_id)
#                     user = SqlAlchemyRepository.get_user_by_id(user_id)
#
#                     review = Review(user, game, rating, review_text)
#
#                     self.__dataset_of_reviews.append(review)
#                     print(self.__dataset_of_reviews)
#
#                 except ValueError as e:
#                     print(f"Skipping row due to invalid data: {e}")
#                 except KeyError as e:
#                     print(f"Skipping row due to missing key: {e}")
#
#
#     def get_unique_reviews_count(self):
#         return len(self.__dataset_of_reviews)
#
#     @property
#     def dataset_of_reviews(self) -> list:
#         return self.__dataset_of_reviews

