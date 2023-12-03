from flask import Blueprint, render_template, redirect, url_for, session, request
import games.browse.services as services
import games.adapters.repository as repo
import games.profile.profile as profile

browse_blueprint = Blueprint(
    'games_bp', __name__)

# @browse_blueprint.route('/browse', methods=['GET'])
# def browse_games():
#     num_games = services.get_number_of_games(repo.repo_instance)
#     all_games = services.get_games(repo.repo_instance)
#     return render_template(
#         'browse.html',
#         # custom page title 
#         title = f'Browse Games | CS235 Game Library',
#         #page heading 
#         heading = 'Browse games',
#         games = all_games,
#         num_games = num_games,
#     )

@browse_blueprint.route('/browse_games', methods=['GET'])
def browse_games():

    games_per_page = 20


    page = request.args.get('page')
    page = int(page) if page is not None and page.isdigit() else 0

    num_games = services.get_number_of_games(repo.repo_instance)
    page_games = services.get_games_for_page(
        page, games_per_page, repo.repo_instance)

    first_games_url, prev_games_url, next_games_url, last_games_url = None, None, None, None

    # Previous page
    if page > 0:
        prev_games_url = url_for('games_bp.browse_games', page=page - 1)
        first_games_url = url_for('games_bp.browse_games')

    # Next page
    if page * games_per_page + games_per_page < num_games:
        next_games_url = url_for('games_bp.browse_games', page=page+1)
        # Last page
        last_games_url = url_for(
            'games_bp.browse_games', page=(num_games-1)//games_per_page)

    # Get the user's wishlist from the session
    user_wishlist = session.get('wishlist', [])

    return render_template(
        'browse.html',
        # Custom page title
        title=f'Browse Games | CS235 Music Library',
        # Page heading
        heading='Browse Games',
        page=page,
        games=page_games,
        first_games_url=first_games_url,
        prev_games_url=prev_games_url,
        next_games_url=next_games_url,
        last_games_url=last_games_url,
        user_wishlist=user_wishlist
    )

        