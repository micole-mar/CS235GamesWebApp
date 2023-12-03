# games.profile.services.py

from games.domainmodel.model import Game, User, Wishlist
from games.adapters.repository import AbstractRepository

# services.py

def add_game_to_wishlist(repo: AbstractRepository, user: User, game_id: Game):
    game = repo.get_game_by_id(game_id)
    if game:
        user.add_favourite_game(game)
        repo.add_favourite_game(game)
        return True
    return False

def remove_game_from_wishlist(repo: AbstractRepository, user: User, game_id: Game):
    game = repo.get_game_by_id(game_id)
    if game:
        user.remove_favourite_game(game)
        repo.remove_favourite_game(game)
        return True
    return False
