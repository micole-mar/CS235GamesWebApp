from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, make_review, User, Review
from typing import List, Iterable

class NonExistentGameException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def add_review(game_id: int, review_text: str, username: str, rating: int, repo: AbstractRepository):
    
    game = repo.get_game_by_id(game_id)
    if game is None:
        raise NonExistentGameException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(user, game, rating, review_text)

    # Update the repository.
    repo.add_review(review)

    user.add_review(review)

def get_reviews_for_game(game_id, repo: AbstractRepository):
    game = repo.get_game_by_id(game_id)

    if game is None:
        raise NonExistentGameException

    return reviews_to_dict(game.reviews)

def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        game_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'description': game.description,
            'publisher': game.publisher,
            'image': game.image_url,
            'release_date': game.release_date,
            'reviews': reviews_to_dict(game.reviews),
            'genres': game.genres,
        }
        game_dicts.append(game_dict)
    return game_dicts

def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.username,
        'game_id': review.game.game_id,
        'review_text': review.comment,
    }
    return review_dict
def game_to_dict(game: Game):
    game_dict = {
        'game_id': game.game_id,
            'title': game.title,
            'description': game.description,
            'publisher': game.publisher,
            'image': game.image_url,
            'release_date': game.release_date,
            'reviews': reviews_to_dict(game.reviews),
            'genres': game.genres,
    }
    return game_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]

def get_game_by_id(repo, game_id):
     return repo.get_game_by_id(game_id)

def get_game(game_id: int, repo: AbstractRepository):
    game = repo.get_game_by_id(game_id)

    if game is None:
        raise NonExistentGameException

    return game_to_dict(game)

#
# def get_reviews_for_game(repo, game_id):
#     game_id = int(game_id)  # Ensure game_id is an integer
#     return repo.get_reviews_for_game(game_id)


