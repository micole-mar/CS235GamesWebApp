import unittest
import tempfile
import csv
from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Publisher, Genre, Game, User, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class TestMemoryRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MemoryRepository()
        populate(self.repository)

    def test_repository_can_add_and_retrieve_game_object(self):
        test_game = Game(888, "Barbie Life in the Dream House") # Make up a new test game
        self.repository.add_game(test_game)  # Add the game to the repository
        retrieved_game = self.repository.get_game_by_id(888)
        self.assertEqual(test_game, retrieved_game)

    def test_repository_retrieves_number_of_game_objects(self):
        # Use repository to fetch the actual data
        actual_game_count = self.repository.get_number_of_games()  # Adjust this to match your repository method
        expected_game_count = 877  # Expected count from actual csv
        # Check if the actual count matches the expected count
        self.assertEqual(actual_game_count, expected_game_count)

    def test_number_of_unique_genres_in_dataset(self):
        # Use repository to fetch the actual data
        actual_games = self.repository.get_games()
        # Extract and count unique genres from the actual dataset
        unique_genres = set()
        for game in actual_games:
            unique_genres.update(game.genres)
        # Check if the number of unique genres matches the expected count
        self.assertEqual(len(unique_genres), 24)

    def test_repository_adds_new_genre_and_count_increases(self):
        # Test that the repository adds a new genre, and the count of genres increases by 1
        orig_unique_genres = self.repository.get_unique_genres()
        test_genre = Genre("Everything Barbie")
        self.repository.add_genre(test_genre)
        unique_genres = self.repository.get_unique_genres()
        expected_count = len(orig_unique_genres) + int(1)
        self.assertEqual(len(unique_genres), expected_count)

    def test_search_games_by_title(self):
        # Test repository search games by title
        # Search for a game by title
        result_by_title = self.repository.search_by_title("MURI")
        # Check if the search result contains the expected game(s)
        self.assertEqual(len(result_by_title), 1)
        self.assertEqual(result_by_title[0], self.repository.get_game(267360))

    def test_search_games_by_publisher(self):
        # Test repository search games by title
        # Search for a game by publisher
        result_by_publisher = self.repository.search_games_by_publisher("Ludosity")
        # Check if the search result contains the expected game(s)
        self.assertEqual(len(result_by_publisher), 1)
        self.assertEqual(result_by_publisher[0], self.repository.get_game(267360))

    def test_search_games_by_genre(self):
        # Test repository search games by genre
        genre_name = "Action"  # will test for action genre
        result_by_genre = self.repository.search_games_by_genre(genre_name)
        # Check if the search result contains at least one game with the specified genre
        self.assertTrue(len(result_by_genre) > 0)
        # Verify that all games in the result have the correct genre
        for game in result_by_genre:
            # Check if the genre_name is present in lowercase in any of the game's genres
            self.assertTrue(any(genre_name.lower() in str(genre).lower() for genre in game.genres))

    def test_get_games_by_genre(self):
        # Test repository get games by genre
        genre_name = "Action"
        result_by_genre = self.repository.get_games_by_genre(genre_name)
        # Check if the search result contains at least one game with the specified genre
        self.assertTrue(len(result_by_genre) > 0)
        # Verify that all games in the result have the correct genre
        for game in result_by_genre:
            # Check if the genre_name is present in lowercase in any of the game's genres
            self.assertTrue(any(genre_name.lower() in str(genre).lower() for genre in game.genres))

    def test_repository_get_games_by_invalid_genre(self):
        # Search for games by an invalid genre name
        results = self.repository.search_games_by_genre("Invalid Genre")
        self.assertEqual(len(results), 0) # There should be no games with the invalid genre

    def test_get_reviews_for_nonexistent_game(self):
        # Try to retrieve reviews for a game that doesn't exist in the repository
        retrieved_reviews = self.repository.get_reviews_for_game(999)
        # Ensure that the retrieved reviews list is empty
        self.assertEqual(len(retrieved_reviews), 0)

    def test_get_game_by_id_existing(self):
        # Test when the game ID exists in the repository
        game_id = 7940
        expected_game = self.repository.get_game(game_id)
        retrieved_game = self.repository.get_game_by_id(game_id)
        self.assertEqual(retrieved_game, expected_game)

    def test_get_game_by_id_non_existing(self):
        # Test when the game ID does not exist in the repository
        game_id = 999999  # id that does not exist in the repo
        retrieved_game = self.repository.get_game_by_id(game_id)
        self.assertIsNone(retrieved_game)  # The result should be None

    def test_add_review(self):
        # Test adding a review to a game
        game_id = 7940  # id for existing game in repo
        user = User("username", "password")
        comment = "Amazing game!! Will definitely recommend!"
        test_game = self.repository.get_game_by_id(game_id)
        review = Review(user, test_game, 5, comment)
        self.repository.add_review(review)  # Add the review to the game
        retrieved_reviews = self.repository.get_reviews_for_game(game_id)  # Get reviews for the game
        self.assertTrue(review in retrieved_reviews)  # Check if the added review is in the retrieved reviews

    def test_add_user_and_get_user(self):
        # Test adding a user to the repository and retrieving it
        user = User("test_user", "password")
        self.repository.add_user(user)
        retrieved_user = self.repository.get_user("test_user")
        self.assertEqual(user, retrieved_user)

    def test_get_favourite_game(self):
        # Test getting a favorite game for a user
        user = User("test_user", "password")
        game = Game(7940, "Call of DutyÂ® 4: Modern WarfareÂ®")
        self.repository.add_user(user)
        self.repository.add_favourite_game(game)
        retrieved_game = self.repository.get_favourite_game(user, 7940)
        self.assertEqual(game, retrieved_game)
        #

    def test_get_reviews_for_game(self):
        # Test retrieving reviews for a specific game
        user1 = User("user1", "password1")
        user2 = User("user2", "password2")
        game = Game(7940, "Call of DutyÂ® 4: Modern WarfareÂ®")
        review1 = Review(user1, game, 5, "Excellent game!")
        review2 = Review(user2, game, 3, "Good game, but could be better.")
        self.repository.add_review(review1)
        self.repository.add_review(review2)
        retrieved_reviews = self.repository.get_reviews_for_game(7940)
        self.assertEqual(len(retrieved_reviews), 2)


class TestPopulate(unittest.TestCase):
    # test populate
    def test_populate(self):
        # Create a temporary directory to store the test CSV file
        temp_dir = tempfile.TemporaryDirectory()
        try:
            # Create a new MemoryRepository for test
            repo_test = MemoryRepository()
            # Test CSV file with sample data in the temporary directory
            test_csv_file = temp_dir.name + '/test_games.csv'
            with open(test_csv_file, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                # Sample CSV data, similar to actual CSV structure
                csv_writer.writerow(['AppID', 'Name', 'Release date', 'Price', 'About the game', 'Supported languages',
                                     'Reviews', 'Header image', 'Website', 'Windows', 'Mac', 'Linux',
                                     'Achievements', 'Recommendations', 'Notes', 'Developers', 'Publishers',
                                     'Categories',
                                     'Genres', 'Tags', 'Screenshots', 'Movies'])
                csv_writer.writerow(
                    [1, 'Test Game 1', 'Aug 31, 2023', '13.33', 'Sample game description', "['English']",
                     '', 'image.jpg', 'http://example.com', 'True', 'True', 'False',
                     '0', '0', ' ', 'Sample', 'Sample', 'Single-player,Multi-player',
                     'Action,Adventure', ' ', 'screenshot1.jpg,screenshot2.jpg', 'http://example.com'])
            # Create a GameFileCSVReader and read the test CSV file
            reader = GameFileCSVReader(test_csv_file)
            reader.read_csv_file()
            # Add games to the repo_test, and let the MemoryRepository handle genre extraction
            for game in reader.dataset_of_games:
                repo_test.add_game(game)
                for genre in game.genres:
                    repo_test.add_genre(genre)
            # Assert that the new repository contains the expected number of games and genres
            self.assertEqual(len(repo_test.get_games()), 1)
            expected_game = repo_test.get_game_by_id(1)
            self.assertIsNotNone(expected_game)  # Ensure the game is not None
        finally:
            # Clean up the temporary directory and its contents
            temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()
