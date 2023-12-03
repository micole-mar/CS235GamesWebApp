from flask import Blueprint, render_template, redirect, url_for, session, request
import games.home.services as services
import games.adapters.repository as repo


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    featured_games = services.get_featured_games(repo.repo_instance)
    return render_template(
        'home.html',
        games=featured_games,
        
    )
