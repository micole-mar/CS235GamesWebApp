import os
from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader #, UserFileCSVReader # ReviewFileCSVReader


def populate(data_path: Path, repo: AbstractRepository):

    games_file_name = str(Path(data_path) / "games.csv")

    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    publishers = reader.dataset_of_publishers
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres

    # Add publishers to the repo
    repo.add_multiple_publishers(publishers)

    # Add genres to the repo
    repo.add_multiple_genres(genres)

    # Add games to the repo
    repo.add_multiple_games(games)

    # ## populate users file
    #
    # users_file_name = str(Path(data_path) / "users.csv")
    # reader = UserFileCSVReader(users_file_name)
    # reader.read_csv_file()
    # users = reader.dataset_of_users
    # repo.add_multiple_users(users)

    # ## populate reviews file
    #
    # reviews_file_name = str(Path(data_path) / "reviews.csv")
    # reader = ReviewFileCSVReader(reviews_file_name)
    # reader.read_csv_file()
    # reviews = reader.dataset_of_reviews
    # repo.add_multiple_reviews(reviews)
    #

    # Not sure whether im supposed to add reviews and users here to this file ???????


# need to populate reviews and users from csv