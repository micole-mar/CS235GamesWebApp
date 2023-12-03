from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game
from games.domainmodel.model import Genre

class InvalidPageException(Exception):
    pass

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        game_dict = {
            'game_id':game.game_id,
            'title': game.title,
            'game_url': game.release_date,
            'game_price': game.price
        }
        game_dicts.append(game_dict)

    return game_dicts

def get_games_for_page(page_index: int, games_per_page: int, repo: AbstractRepository):
    if type(page_index) is not int:
        raise InvalidPageException('Page should be a type integer')
    if page_index < 0:
        raise InvalidPageException('Negative page does not exist.')

    games = repo.get_games()

    start_index = page_index * games_per_page
    if start_index >= len(games):
        raise InvalidPageException('The page does not exist.')

  
    games_for_page = games[start_index:start_index+games_per_page]
    game_dicts = []
    for game in games_for_page:
        thegenres = " "
       
        for thing in game.genres:
            thegenres += (' '+thing.genre_name+",")
        

        game_dict = {
            'game_id':game.game_id,
            'title': game.title,
            'game_url': game.release_date,
            'image_url': game.image_url,
            'genres': thegenres,
            'publisher': game.publisher.publisher_name,
            'price': game.price
        }
        game_dicts.append(game_dict)

    return game_dicts