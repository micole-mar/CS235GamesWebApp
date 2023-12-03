from sqlalchemy import select, inspect

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'games', 'genres', 'publishers', 'reviews',
                                           'user_wishlist', 'users']


def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]
    print(name_of_genres_table)

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        print(select_statement)
        print(result) # nothing is in the result

        all_genre_names = []
        for row in result:
            print("print test", row)
            all_genre_names.append(row['genre_name'])

        print('genre names:', all_genre_names)
        print(len(all_genre_names))

        # change genre names from covid tag names to game genre names
        assert sorted(all_genre_names) == sorted(
            ['Casual', 'Design & Illustration', 'Game Development', 'Adventure', 'Action',
             'Sports', 'Software Training', 'Utilities', 'Gore', 'Animation & Modeling',
             'Audio Production', 'Racing', 'Simulation', 'Violent', 'Web Publishing',
             'Free to Play', 'Indie', 'Education', 'Massively Multiplayer', 'Strategy',
             'Early Access', 'Video Production', 'RPG', 'Photo Editing'])


# def test_database_populate_select_all_users(database_engine):
#
#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_users_table = inspector.get_table_names()[6]
#     print('name of users table: ', name_of_users_table)
#
#     with database_engine.connect() as connection:
#         # query for records in table users
#         select_statement = select([metadata.tables[name_of_users_table]])
#         result = connection.execute(select_statement)
#         print("select statement:", select_statement)
#         print("result: ", result) # nothing is in the result
#         print("result type: ", type(result))
#         print("size: ", result.__sizeof__())
#
#         all_users = [row['username'] for row in result]
#         print(all_users)
#
#         assert all_users == ['cs_student', 'johndoe'] # need to see where usernames are from


def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[3]
    print('name_of_ rev table: ', name_of_reviews_table)

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append((row['name']))
        all_publishers = sorted(all_publishers)

        assert len(all_publishers) == 798
        assert all_publishers[0] == '13-lab,azimuth team'
        assert all_publishers[-1] == '路过的骑士皇'

# # not necessary
# def test_database_populate_select_all_reviews(database_engine):
#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_reviews_table = inspector.get_table_names()[2]
#
#     with database_engine.connect() as connection:
#         # query for records in table comments
#         select_statement = select([metadata.tables[name_of_reviews_table]])
#         result = connection.execute(select_statement)
#
#         all_reviews = []
#         for row in result:
#             all_reviews.append((row['review_id'], row['user_id'], row['game_id'], row['review_text'], row['rating']))
#
#         assert all_reviews == [(1,2,7940,'this game is so fun! everyone should try it!!',5)]


def test_database_populate_select_all_games(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]
    print("db engine:", database_engine)
    print("inspector:", inspector)
    print("name of games table:", name_of_games_table)

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        print('print test', select_statement)
        print('print test result:', result)
        for row in result:
            print('print test row:', row)
            all_games.append((row['game_id']))
        print('print test all games:', all_games)
        nr_games = len(all_games)
        print("print test", nr_games, "number of games")
        assert nr_games == 877

        assert all_games[0] == 3010
