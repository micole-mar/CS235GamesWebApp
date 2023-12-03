from typing import List
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

# def search_by_title(repo: AbstractRepository, title: str) -> List[Game]:
#     title = title.lower()
#     return [game for game in repo.get_games() if title in game.title.lower()]

def search_by_type(repo: AbstractRepository, query: str, search_type: str) -> List[Game]:
    query = query.lower()

    all_games = repo.get_games()
    search_results = []

    for game in all_games:
        if search_type == 'title' and query in game.title.lower():
            search_results.append(game)
        elif search_type == 'genre':
            for genre in game.genres:
                if query == str(genre.genre_name.lower()):
                    search_results.append(game)
        elif search_type == 'publisher' and game.publisher and query in game.publisher.publisher_name.lower():
            search_results.append(game)

    return search_results


# def search_games_based_on_query_and_genre(repo: AbstractRepository, query: str, selected_genre: str) -> List[Game]:
#     query = query.lower()
#     search_results = []
#     all_games = repo.get_games()
#     # Filter based on query
#     # search_results = [game for game in all_games if query in game.title.lower()]
#
#     # Filter further based on selected genre
#     if selected_genre != 'none':
#         search_results = list()
#         for game in all_games:
#             for genre in game.genres:
#                 if selected_genre == str(genre) and query in game.title.lower():
#                     search_results.append(game)
#
#     return search_results
