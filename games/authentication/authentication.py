from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps
from games.adapters.memory_repository import load_users
from pathlib import Path
import games.authentication.services as services
import games.adapters.repository as repo
import csv


# Configure Blueprint
authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')
data_path = "games/adapters/data"

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        try:
            # Registration is successful
            services.add_user(form.username.data, form.password.data, repo.repo_instance)
            flash('Registration successful!', 'success')  # Add a success flash message
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            username_not_unique = 'Your username is already taken - please supply another'

    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        username_error_message=username_not_unique,
        handler_url=url_for('authentication_bp.register'),
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_not_exist = None
    incorrect_password = None

    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo.repo_instance)
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)
            session.clear()
            session['username'] = user['username']
            flash('Login successful!', 'success')  # Add a success flash message
            return redirect(url_for('home_bp.home'))
        except services.AuthenticationException:
            incorrect_password = "Incorrect password, please try again"
            flash('Login failed. Incorrect password.', 'danger')  # Add a danger flash message
        except services.UnknownUserException:
            username_not_exist = "Unrecognizable username, please supply another"
            flash('Login failed. Unknown username.', 'danger')  # Add a danger flash message


    return render_template('authentication/credentials.html', title='Login',
                           username_error_message=username_not_exist,
                           password_error_message=incorrect_password,
                           form=form
                           )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    flash('Logout successful!', 'success')  # Add a success flash message
    return redirect(url_for('home_bp.home'))



def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))

        user = services.get_user(session['username'], repo.repo_instance)
        # If the user does not exist (while the session is still there), redirect to the register page.
        if not user:
            session.clear()
            return redirect(url_for('authentication_bp.register'
                                    ))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
           a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register', render_kw={"class": "submit"})


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [
        DataRequired(),
        PasswordValid()
    ])
    submit = SubmitField('Login', render_kw={"class": "submit"})
