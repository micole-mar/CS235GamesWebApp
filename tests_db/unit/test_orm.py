import pytest


from datetime import date, datetime

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import User, Game, Review, Publisher, Genre, make_review
from sqlalchemy.exc import IntegrityError
import games.adapters.orm as repo



from datetime import date, datetime



def insert_user(empty_session, values=None):
    new_name = "andrew"
    new_password = "1234567"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def make_user():
    user = User("andrew", "1111111")
    return user

def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234567"))
    users.append(("cindy", "1111111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234567"),
        User("cindy", "9999999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("andrew", "1111111")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("andrew", "1234567"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "1111111")
        empty_session.add(user)
        empty_session.commit()


#------game tests section ---#

def make_game():
    game = Game(
        7940,"Call of DutyÂ® 4: Modern WarfareÂ®"
    )
    game.price = 14.99
    game.release_date = "Nov 12, 2007"
    game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of the Call of DutyÂ® series, delivers the most intense and cinematic action experience ever. Call of Duty 4: Modern Warfare arms gamers with an arsenal of advanced and powerful modern day firepower and transports them to the most treacherous hotspots around the globe to take on a rogue enemy group threatening the world. As both a U.S Marine and British S.A.S. soldier fighting through an unfolding story full of twists and turns, players use sophisticated technology, superior firepower and coordinated land and air strikes on a battlefield where speed, accuracy and communication are essential to victory. The epic title also delivers an added depth of multiplayer action providing online fans an all-new community of persistence, addictive and customizable gameplay. Authentic Advanced Weaponry."
    game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    game.screenshots = "https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002987.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002988.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002989.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002990.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002991.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002992.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002993.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002994.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002995.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002996.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002997.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002998.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002999.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000003000.1920x1080.jpg?t=1646762118"
    game.website_url = "http://www.charlieoscardelta.com/"
    game.windows = True
    game.mac = True
    game.linux = True
    game.developers = "Infinity Ward"

    game.player_modes = "Single-player,Multi-player"
    
    game.recommendations = 13199
    game.movie_url= "http://cdn.akamai.steamstatic.com/steam/apps/256803408/movie_max.mp4?t=1601679223"
    return game 
    

def insert_game(empty_session):
    empty_session.execute(
        'INSERT INTO games (game_id, game_title, game_price, release_date, game_description, game_image_url, game_website_url, game_windows, game_mac, game_linux, game_movie_url, game_recommendations, game_screenshots, game_languages, game_player_modes, game_developers) VALUES '
'(7940, "Call of DutyÂ® 4: Modern WarfareÂ®", 14.99, "Nov 12, 2007", '
'"The new action-thriller from the award-winning team at Infinity Ward, the creators of the Call of DutyÂ® series, delivers the most intense and cinematic action experience ever. Call of Duty 4: Modern Warfare arms gamers with an arsenal of advanced and powerful modern day firepower and transports them to the most treacherous hotspots around the globe to take on a rogue enemy group threatening the world. As both a U.S Marine and British S.A.S. soldier fighting through an unfolding story full of twists and turns, players use sophisticated technology, superior firepower and coordinated land and air strikes on a battlefield where speed, accuracy and communication are essential to victory. The epic title also delivers an added depth of multiplayer action providing online fans an all-new community of persistence, addictive and customizable gameplay. Authentic Advanced Weaponry.", '
'"https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118", '
'"http://www.charlieoscardelta.com/", TRUE, TRUE, TRUE, '
'"http://cdn.akamai.steamstatic.com/steam/apps/256803408/movie_max.mp4?t=1601679223", '
'13199, "https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002987.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002988.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002989.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002990.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002991.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002992.1920x1080.jpg?t=1646762118","https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002993.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002994.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002995.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002996.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002997.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002998.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002999.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000003000.1920x1080.jpg?t=1646762118", '
'"Single-player,Multi-player", "Infinity Ward")'

    )
    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]


def test_loading_of_game(empty_session):
    game_key = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_key == fetched_game.game_id

   
def test_saving_of_game(empty_session):
     game = make_game()
     empty_session.add(game)
     empty_session.commit()

     rows = list(empty_session.execute('SELECT game_id, game_title, game_price, release_date, game_description, game_image_url, game_website_url, game_windows, game_mac, game_linux, game_movie_url, game_recommendations, game_screenshots, game_player_modes, game_developers  FROM games'))
     print(rows)
     assert rows == [(7940, 'Call of DutyÂ® 4: Modern WarfareÂ®', 14.99, 'Nov 12, 2007', 'The new action-thriller from the award-winning team at Infinity Ward, the creators of the Call of DutyÂ® series, delivers the most intense and cinematic action experience ever. Call of Duty 4: Modern Warfare arms gamers with an arsenal of advanced and powerful modern day firepower and transports them to the most treacherous hotspots around the globe to take on a rogue enemy group threatening the world. As both a U.S Marine and British S.A.S. soldier fighting through an unfolding story full of twists and turns, players use sophisticated technology, superior firepower and coordinated land and air strikes on a battlefield where speed, accuracy and communication are essential to victory. The epic title also delivers an added depth of multiplayer action providing online fans an all-new community of persistence, addictive and customizable gameplay. Authentic Advanced Weaponry.', 'https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118', 'http://www.charlieoscardelta.com/', '1', '1', '1', 'http://cdn.akamai.steamstatic.com/steam/apps/256803408/movie_max.mp4?t=1601679223', 13199, 'https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002987.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002988.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002989.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002990.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002991.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002992.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002993.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002994.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002995.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002996.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002997.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002998.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000002999.1920x1080.jpg?t=1646762118,https://cdn.akamai.steamstatic.com/steam/apps/7940/0000003000.1920x1080.jpg?t=1646762118', 'Single-player,Multi-player', 'Infinity Ward')] 


   # ---- Reviews -----
   
def insert_reviewed_game(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)

    
    empty_session.execute(
        'INSERT INTO reviews (user_id, game_id, review_text, rating) VALUES '
        '(:user_id, :game_id, "Review 1", 2),'
        '(:user_id, :game_id, "Review 2", 3)',
        {'user_id': user_key, 'game_id': game_key,}
    )

    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]


def test_loading_of_reviewed_game(empty_session):
    insert_reviewed_game(empty_session)

    rows = empty_session.query(Game).all()
    game = rows[0]

    for review in game.reviews:
        assert review.game is game


def test_saving_of_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("andrew", "1234567"))

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__username == "andrew").one()

    
    review_texty = "Some review text."
    rating = 3
    review = make_review( user, game, rating, review_texty)
    
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, review_text, rating FROM reviews'))

    assert rows == [(user_key, game_key, review_texty, rating)]


def test_save_reviewed_game(empty_session):
   
    game = make_game()
    user = make_user()

    
    review_texty = "Some review text."
    rating = 3
    review = make_review( user, game, rating, review_texty)

    
    empty_session.add(game)
    empty_session.commit()


    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]


    rows = list(empty_session.execute('SELECT user_id FROM users'))
    user_key = rows[0][0]


    rows = list(empty_session.execute('SELECT user_id, game_id, review_text, rating FROM reviews'))
    assert rows == [(user_key, game_key, review_texty, rating)]

# publisher



def make_publisher():
    publisher = Publisher("bob")
    return publisher

def insert_publisher(empty_session):
    empty_session.execute(
        'INSERT INTO publishers (name) VALUES '
        '("bob")'

    )
    row = empty_session.execute('SELECT name from publishers').fetchone()
    return row[0]

def test_loading_of_publisher(empty_session):
    game_publisher = insert_publisher(empty_session)
    expected_name = make_publisher()
    fetched_publisher = empty_session.query(Publisher).one()

    assert expected_name == fetched_publisher
    assert game_publisher == fetched_publisher.publisher_name

def test_saving_of_publisher(empty_session):
     publisher = make_publisher()
     empty_session.add(publisher)
     empty_session.commit()

     rows = list(empty_session.execute('SELECT name FROM publishers'))
     print(rows)
     assert rows == [('bob',)] 


#genre 

def make_genre():
    genre = Genre("action")
    return genre

def insert_genre(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES '
        '("action")'

    )
    row = empty_session.execute('SELECT genre_name from genres').fetchone()
    return row[0]

def test_loading_of_genre(empty_session):
    game_genre = insert_genre(empty_session)
    expected_name = make_genre()
    fetched_genre = empty_session.query(Genre).one()

    assert expected_name == fetched_genre
    assert game_genre == fetched_genre.genre_name

def test_saving_of_genre(empty_session):
     genre = make_genre()
     empty_session.add(genre)
     empty_session.commit()

     rows = list(empty_session.execute('SELECT genre_name FROM genres'))
     print(rows)
     assert rows == [('action',)] 


