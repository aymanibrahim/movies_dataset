import unittest
import os
from movie_dataset import MovieDataset
from genre_extractor import GenreExtractor
from director_extractor import DirectorExtractor


class TestMovieDataset(unittest.TestCase):

    def setUp(self):
        # sample data files
        self.metadata_file = "data/sample_data/sample_metadata.csv"        
        self.credits_file = "data/sample_data/sample_credits.csv"
        self.ratings_file = "data/ratings_small.csv"
        
        self.dataset = MovieDataset(self.metadata_file, self.ratings_file, self.credits_file)

    def test_unique_movies(self):
        unique_movies = self.dataset.unique_movies()
        self.assertIsInstance(unique_movies, int)
        self.assertGreater(unique_movies, 0)
        self.assertEqual(unique_movies, 2830)

    def test_average_rating(self):
        average_rating = self.dataset.average_rating()
        self.assertAlmostEqual(average_rating, 3.3, delta=0.1)

    def test_top_rated_movies(self):
        top_rated_movies = self.dataset.top_rated_movies(n=5)
        expected_titles = ['The Wizard', 'Rio Bravo', 'The Celebration', 'Spider-Man 3', 'A Streetcar Named Desire']
        self.assertListEqual(top_rated_movies['title'].tolist(), expected_titles)

    def tearDown(self):
        pass


class TestGenreExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = GenreExtractor()

    def test_extract_genre(self):
        sample_genre_data = '[{"id": 18, "name": "Drama"}, {"id": 35, "name": "Comedy"}, {"id": 10749, "name": "Romance"}]'
        expected_genres = ['Drama', 'Comedy', 'Romance']
        extracted_genres = self.extractor.extract_genre(sample_genre_data)
        self.assertListEqual(extracted_genres, expected_genres)

    def test_extract_genre_empty(self):
        sample_genre_data = '[]'
        expected_genres = []
        extracted_genres = self.extractor.extract_genre(sample_genre_data)
        self.assertListEqual(extracted_genres, expected_genres)

    def test_extract_genre_invalid(self):
        sample_genre_data = 'invalid_data'
        expected_genres = []
        extracted_genres = self.extractor.extract_genre(sample_genre_data)
        self.assertListEqual(extracted_genres, expected_genres)

    def tearDown(self):
        pass


class TestDirectorExtractor(unittest.TestCase):

    def test_extract_director(self):
        crew_data = '[{"credit_id": "52fe4284c3a36847f8024f49", "department": "Directing", "gender": 2, "id": 7879, "job": "Director", "name": "John Lasseter", "profile_path": "/7EdqiNbr4FRjIhKHyPPdFfEEEFG.jpg"}]'
        director_extractor = DirectorExtractor()
        director = director_extractor.extract_director(crew_data)
        self.assertEqual(director, "John Lasseter")

    def test_extract_director_no_director(self):
        crew_data = '[{"credit_id": "52fe4284c3a36847f8024f49", "department": "Writing", "gender": 2, "id": 7879, "job": "Writer", "name": "John Lasseter", "profile_path": "/7EdqiNbr4FRjIhKHyPPdFfEEEFG.jpg"}]'
        director_extractor = DirectorExtractor()
        director = director_extractor.extract_director(crew_data)
        self.assertIsNone(director)

    def test_extract_director_invalid_data(self):
        crew_data = '{"invalid_data"}'
        director_extractor = DirectorExtractor()
        director = director_extractor.extract_director(crew_data)
        self.assertEqual(director, [])

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
