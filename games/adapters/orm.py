from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean,
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, Review, User, Wishlist

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    # We only want to maintain those attributes that are in our domain model
    # For publisher, we only have name.
    Column('name', String(255), primary_key=True)  # nullable=False, unique=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float),
    Column('release_date', String(50)),
    Column('game_description', Text, nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    # add columns
    Column('game_windows', Text),
    Column('game_mac', Text),
    Column('game_linux', Text),
    Column('game_movie_url', String(1000)),
    Column('game_recommendations', Integer),
    Column('publisher_name', ForeignKey('publishers.name')),
    Column('game_screenshots', Text),
    Column('game_languages', Text),
    Column('game_player_modes', Text),
    Column('game_developers', Text)
)

genres_table = Table(
    'genres', metadata,
    # For genre again we only have name.
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

users_table = Table(
    'users' , metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(20), unique=True, nullable=False),
    Column('password', String(20), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    # Column('timestamp', DateTime, nullable=False),
    Column('game_id', ForeignKey('games.game_id')),
    Column('user_id', ForeignKey('users.user_id')),
    Column('review_text', String(255), nullable=False),
    Column('rating', Integer, nullable= False),
)

user_wishlist_table = Table(
    'user_wishlist' , metadata,
    Column('id', Integer, primary_key=True, autoincrement=True ),
    Column('game_id', ForeignKey('games.game_id')),
    Column('user_id', ForeignKey('users.user_id'))
)

def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_User__favourite_games': relationship(Game, secondary=user_wishlist_table)
    })

    mapper(Review, reviews_table, properties={
        # '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__comment': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__game': relationship(Game, back_populates='_Game__reviews')
    })


    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__reviews': relationship(Review, back_populates='_Review__game'),
        '_Game__windows': games_table.c.game_windows,
        '_Game__mac': games_table.c.game_mac,
        '_Game__linux': games_table.c.game_linux,
        '_Game__movie_url': games_table.c.game_movie_url,
        '_Game__recommendations': games_table.c.game_recommendations,
        '_Game__screenshots': games_table.c.game_screenshots,
        '_Game__languages': games_table.c.game_languages,
        '_Game__player_modes': games_table.c.game_player_modes,
        '_Game__developers': games_table.c.game_developers,
    })