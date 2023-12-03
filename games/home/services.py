from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game
from games.domainmodel.model import Genre





def get_featured_games(repo: AbstractRepository):


    games = repo.get_games()

  
    games_for_page = games[0:4]
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
        }
        game_dicts.append(game_dict)

    return game_dicts
