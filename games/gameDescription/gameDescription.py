from flask import Blueprint, render_template, redirect, url_for, session, request

import games.gameDescription.services as services
import games.adapters.repository as repo
from games.domainmodel.model import Game, Review, User

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from games.authentication.authentication import login_required

gameDescription_blueprint = Blueprint(
    'gameDescription_bp', __name__)


@gameDescription_blueprint.route('/gameDescription/<int:game_id>', methods=['GET'])
def game_description(game_id):
    game = services.get_game_by_id(repo.repo_instance, game_id)
    return render_template('gameDescription.html', game=game, )


@gameDescription_blueprint.route('/review/<int:game_id>', methods=['GET', 'POST'])
@login_required
def review_on_games(game_id):
    username = session.get('username') if 'username' in session else None
    form = ReviewForm()

    if form.validate_on_submit():
        services.add_review(game_id, form.review.data, username, form.rating.data, repo.repo_instance)

        # game = services.get_game_by_id(game_id, repo.repo_instance)

        return redirect(url_for('gameDescription_bp.game_description', game_id=game_id))
    return render_template('review_on_game.html', form=form)


##########
# if request.method == 'GET':
# Request is a HTTP GET to display the form.
# Extract the article id, representing the article to comment, from a query parameter of the GET request.
# game_id = int(request.args.get('game'))
# pass

# form.game_id.data = game_id
# else:
# pass
# game_id = int(form.game_id.data)


# game_id = int(form.game_id.data)
# if game_id is not None:

# game = services.get_game_by_id(game_id, repo.repo_instance)
# return render_template(
#    '/review_on_game.html',
#    title='Edit game',
#   game=game,
#   form=form,
#   handler_url=url_for('gameDescription_bp.review_on_game'),
#   )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')])  # Adjust the range as needed
    game_id = HiddenField("Game id")
    submit = SubmitField('Submit')