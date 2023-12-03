from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import games.profile.services as services
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from games.domainmodel.model import Game, User, Wishlist  # Import your Game model
import games.adapters.repository as repo
from flask import session

from games.authentication.authentication import login_required
import games.profile.services as services

profile_bp = Blueprint("profile_bp", __name__)


# @profile_bp.route('/add_to_wishlist/<int:game_id>', methods=['POST'])
# @login_required
# def add_to_wishlist(game_id):
#     username = session['username']
#     # Get the user from the repository
#     current_user = repo.repo_instance.get_user(username)
#     if current_user:
#
#         # Create a Wishlist object for the user
#         wishlist = Wishlist(current_user)
#
#         # Add the game to the user's wishlist
#         services.add_game(game_id, wishlist, repo.repo_instance)
#
#         flash('Game added to wishlist!', 'success')
#
#     return redirect(url_for('profile_bp.user_profile'))

# @profile_bp.route('/add_to_wishlist/<int:game_id>', methods=['POST'])
# @login_required
# def add_to_wishlist(game_id):
#     username = session['username']
#     # Get the user from the repository
#     current_user = repo.repo_instance.get_user(username)
#     if current_user:
#         game = repo.repo_instance.get_game_by_id(game_id)
#         # Create a Wishlist object for the user
#         current_user.add_favourite_game(game)
#
#         # Add the game to the user's wishlist
#
#         flash('Game added to wishlist!', 'success')
#
#     return redirect(url_for('profile_bp.user_profile'))

@profile_bp.route('/add_to_wishlist/<int:game_id>', methods=['POST'])
@login_required
def add_to_wishlist(game_id):
    username = session['username']
    # Get the user from the repository
    current_user = repo.repo_instance.get_user(username)

    if current_user and services.add_game_to_wishlist(repo.repo_instance, current_user, game_id):
        flash('Game added to wishlist!', 'success')
    else:
        flash('Unable to add the game to wishlist.', 'error')

    return redirect(url_for('profile_bp.user_profile'))

# @profile_bp.route('/remove_from_wishlist/<int:game_id>', methods=['POST'])
# @login_required
# def remove_from_wishlist(game_id):
#     username = session['username']
#     # Get the user from the repository
#     current_user = repo.repo_instance.get_user(username)
#     if current_user:
#         game = repo.repo_instance.get_game_by_id(game_id)
#         # Create a Wishlist object for the user
#         current_user.remove_favourite_game(game)
#
#         # Add the game to the user's wishlist
#
#         flash('Game removed from wishlist!', 'success')
#
#     return redirect(url_for('profile_bp.user_profile'))

@profile_bp.route('/remove_from_wishlist/<int:game_id>', methods=['POST'])
@login_required
def remove_from_wishlist(game_id):
    username = session['username']
    # Get the user from the repository
    current_user = repo.repo_instance.get_user(username)

    if current_user and services.remove_game_from_wishlist(repo.repo_instance, current_user, game_id):
        flash('Game removed from wishlist!', 'success')

    else:
        flash('Unable to remove the game from wishlist.', 'error')

    return redirect(url_for('profile_bp.user_profile'))
@profile_bp.route("/profile")
@login_required
def user_profile():
    username = session['username']

    # Get the user from the repository
    current_user = repo.repo_instance.get_user(username)

    if current_user:
        # Create a Wishlist object for the user
        wishlist = current_user.get_wishlist()
        reviews = current_user.get_reviews()

        return render_template("profile.html", wishlist=wishlist, reviews=reviews)


def get_user_wishlist():
    """
    Retrieve the user's wishlist from the session.

    Returns:
    list: A list of game IDs in the user's wishlist.
    """
    # Check if the 'wishlist' key exists in the session
    if 'wishlist' in session:
        # If it exists, return the wishlist from the session
        print(session['wishlist'])
        return session['wishlist']
    else:
        # If it doesn't exist, return an empty list
        return []