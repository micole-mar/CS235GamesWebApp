"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template, request, url_for, redirect

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from games.domainmodel.model import Game
from games.browse import browse

# local imports
import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.adapters import memory_repository, database_repository, repository_populate
from games.adapters.repository_populate import populate
from games.adapters.orm import metadata, map_model_to_tables



def create_app(test_config=None):
    """Construct the core application."""


     # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']


    # Here the "magic" of our repository pattern happens. We can easily switch between in memory data and
    # persistent database data storage for our application.

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        memory_repository.populate(repo.repo_instance)
        # repository_populate.populate(data_path, repo.repo_instance) #, database_mode)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == True or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            repository_populate.populate(data_path, repo.repo_instance)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()


    with app.app_context():
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from games.gameDescription.gameDescription import gameDescription_blueprint
        app.register_blueprint(gameDescription_blueprint)

        from games.search.search import search_blueprint
        app.register_blueprint(search_blueprint)

        from games.genres.genres import genre_blueprint
        app.register_blueprint(genre_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from games.profile.profile import profile_bp
        app.register_blueprint(profile_bp)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    # repo.repo_instance = MemoryRepository()

    # populate(repo.repo_instance)

    # @app.route('/')
    # def home():
    #     some_game = create_some_game()
    #     # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    #     return render_template('gameDescription.html', game=some_game)

    return app