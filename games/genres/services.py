from typing import List
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game


def get_unique_genres(repo: AbstractRepository) -> List[str]:
    return sorted(repo.get_unique_genres())  # Use repo to get unique genres

def get_games_by_genre(repo: AbstractRepository, genre_name: str) -> List[Game]:
    result = list()

    for game in repo.get_games():  # Use repo to get games
        for genre in game.genres:
            if genre_name == str(genre.genre_name):
                result.append(game)

    return result