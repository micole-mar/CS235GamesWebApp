from flask import Blueprint, render_template
import games.adapters.repository as repo
import games.genres.services as services


# Create a new blueprint for genres
genre_blueprint = Blueprint('genre_bp', __name__)

@genre_blueprint.route('/genre', methods=['GET'])
def genre_list():
    genres_list = services.get_unique_genres(repo.repo_instance)
    return render_template(
        'genre_list.html',
        title='Genres',
        genres_list=genres_list
    )

@genre_blueprint.route('/genre/<genre_name>', methods=['GET'])
def genre_games(genre_name):
    genre_games = services.get_games_by_genre(repo.repo_instance, genre_name)
    return render_template(
        'genre_games.html',
        title=f'{genre_name} Games',
        genre_name=genre_name,
        games=genre_games
    )

