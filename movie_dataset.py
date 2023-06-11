import numpy as np
import pandas as pd
import logging
import warnings

from director_extractor import DirectorExtractor
from genre_extractor import GenreExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

class MovieDataset:
    """A class to process movie dataset"""

    def __init__(self, metadata_file, ratings_file, credits_file):
        """
        Initializes the MovieDataset object by loading and processing data from the given CSV files.

        :param metadata_file: str The path to the metadata CSV file.
        :param ratings_file: str The path to the ratings CSV file.
        :param credits_file: str The path to the credits CSV file.
        """      

        try:
            metadata_df, ratings_df, credits_df = self.load_data(metadata_file, ratings_file, credits_file)
            self.df = self.process_data(metadata_df, ratings_df, credits_df)
            logging.info('Movies dataset created')
        except Exception as e:
            logger.error(f"Error initializing MovieDataset: {e}")
            
    @staticmethod
    def load_data(metadata_file, ratings_file, credits_file):
        """
        Loads data from the given CSV files and returns them as pandas DataFrames.

        :param metadata_file: str The path to the metadata CSV file.
        :param ratings_file: str The path to the ratings CSV file.
        :param credits_file: str The path to the credits CSV file.
        :return: tuple of pd.DataFrame  containing the metadata, ratings and credits DataFrames.
        """
        metadata_df = pd.read_csv(metadata_file)
        ratings_df = pd.read_csv(ratings_file)
        credits_df = pd.read_csv(credits_file)

        logging.info('CSV files loaded')
        return metadata_df, ratings_df, credits_df

    def process_data(self, metadata_df, ratings_df, credits_df):
        """
        Processes the given DataFrames and returns a merged DataFrame.

        :param metadata_df: pd.DataFrame The metadata DataFrame.
        :param ratings_df: pd.DataFrame The ratings DataFrame.
        :param credits_df: pd.DataFrame The credits DataFrame.
        :return: pd.DataFrame The merged DataFrame.
        """
        movies_df = self.preprocess_metadata(metadata_df)
        credits_df = self.preprocess_credits(credits_df)
        ratings_df = self.preprocess_ratings(ratings_df)

        # Merge movies_df and credits_df on the 'id' column
        movies_df = pd.merge(movies_df, credits_df, on='id')

        # Merge movies_df and ratings_df on the 'id' column
        df = pd.merge(movies_df, ratings_df[['id', 'rating']], on='id')
        
        # Select only the required columns
        cols = ['id', 'title', 'release_year', 'director', 'genre', 'rating']
        df = df.loc[:, cols]
        
        # Round the rating score to 1 decimal
        df['rating'] = np.around(df['rating'], decimals=1)
        return df

    @staticmethod
    def preprocess_metadata(metadata_df):
        """
        Preprocesses the metadata DataFrame by extracting relevant columns and processing them.

        :param metadata_df: pd.DataFrame The metadata DataFrame.
        :return: pd.DataFrame movides_df as the preprocessed metadata DataFrame.
        """
        # Use metadata_df columns ['id','title', 'release_date'] to build movies_df dataframe
        cols = ['id', 'title', 'release_date']
        movies_df = metadata_df.loc[:, cols]

        # Convert id into numeric format and filter non-numeric values
        movies_df['id'] = pd.to_numeric(movies_df['id'], errors='coerce')
        movies_df = movies_df[movies_df['id'].notnull()]
        movies_df['id'] = movies_df['id'].astype(int)

        # Extract 'release_year' column from 'release_date'
        movies_df["release_year"] = pd.to_datetime(movies_df["release_date"], errors='coerce').apply(
            lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
        movies_df.drop(columns=['release_date'], inplace=True)

        # Add 'genres' column to movies_df dataframe
        movies_df['genres'] = metadata_df.loc[:, 'genres']

        # Extract genre from the 'genres' column in movies_df
        genre_extractor = GenreExtractor()
        movies_df['genre'] = movies_df['genres'].apply(genre_extractor.extract_genre)
        movies_df.drop(columns=['genres'], inplace=True)

        # Split 'genre' into multiple columns
        genres_split = movies_df['genre'].apply(lambda x: pd.Series(x, dtype=object)).stack().reset_index(level=1,
                                                                                                         drop=True)
        
        # Replace "genres" column with "genre"
        genres_split.name = 'genre'

        # Remove genre list column and add genre column after splitting into multiple rows
        movies_df = movies_df.drop('genre', axis=1).join(genres_split)
        return movies_df

    @staticmethod
    def preprocess_credits(credits_df):
        """
        Preprocesses the credits DataFrame by extracting relevant columns and processing them.

        :param credits_df: pd.DataFrame The credits DataFrame.
        :return: pd.DataFrame The preprocessed credits DataFrame.
        """
        # Extract director from the 'crew' column in credits_df
        director_extractor = DirectorExtractor()
        credits_df['director'] = credits_df['crew'].apply(director_extractor.extract_director)
        credits_df.drop(columns=['crew'], inplace=True)
        return credits_df

    @staticmethod
    def preprocess_ratings(ratings_df):
        """
        Preprocesses the ratings DataFrame by aggregating ratings and converting columns to numeric values.

        :param ratings_df: pd.DataFrame The ratings DataFrame.
        :return: pd.DataFrame The preprocessed ratings DataFrame.
        """
        # Rename 'movieId' column into 'id'
        ratings_df.rename(columns={'movieId': 'id'}, inplace=True)

        # Aggregate ratings by taking the mean for each unique 'id'
        ratings_df = ratings_df.groupby('id', as_index=False)['rating'].mean()

        # Convert 'id' and 'rating' to numeric values
        ratings_df['id'] = pd.to_numeric(ratings_df['id'], errors='coerce')
        ratings_df = ratings_df[ratings_df['id'].notnull()]
        ratings_df = ratings_df.astype({"id": int, "rating": float})
        return ratings_df

    def unique_movies(self):
        """
        Calculate the number of unique movies.
        
        :return: int the number of unique movies.
        """
        return len(self.df['id'].unique())

    def average_rating(self):
        """
        Calculate the average rating of all the movies.
        
        :return: float the average rating of all the movies.
        """        
        return self.df['rating'].mean()

    def top_rated_movies(self, n=5):
        """
        List the top n highest rated movies.
        
        :param n: int the number of movies required (default n=5)
        :return: float the average rating of all the movies.
        """
        # Group by 'id' and calculate the mean rating for each group
        grouped_movies = self.df.groupby(['id', 'title', 'release_year']).mean().reset_index()

        # Return the top n highest-rated movies
        return grouped_movies.nlargest(n, 'rating')
    
    def movies_per_year(self):
        """
        List the number of movies released each year.
        
        :return: pd.DataFrame the number of movies released each year.
        """
        # Filter out rows with missing or invalid release years
        valid_release_years = self.df[self.df['release_year'].notnull() & (self.df['release_year'] != 'NaT')]

        # Group by 'release_year' and count the number of movies
        return valid_release_years.groupby('release_year')['title'].count()


    def movies_per_genre(self):
        """
        List the number of movies in each genre.
        
        :return: pd.DataFrame the number of movies in each genre.
        """
        return self.df['genre'].value_counts()

    def save_to_json(self, json_file):
        """
        Save the dataset to a JSON file
        
        :param json_file: A file path for the JSON file
        """
        try:
            self.df.to_json(json_file, orient='records')
            logging.info('Saving dataset to JSON file completed')
        except Exception as e:
            logger.error(f"Error saving dataset to JSON file: {e}")
            
def main():
    # Set paths of data files
    
    # Full data files
    # metadata_file = "data/movies_metadata.csv"
    # credits_file = "data/credits.csv"    
    # ratings_file = "data/ratings.csv"
    
    # Sample data files
    metadata_file = "data/sample_data/sample_metadata.csv"
    credits_file = "data/sample_data/sample_credits.csv"
    ratings_file = "data/ratings_small.csv"
    
    # Set file path to save dataset in JSON format
    movies_json_file = 'json/movies_dataset.json'
            
    # Process dataset
    try:
        dataset = MovieDataset(metadata_file, ratings_file, credits_file)

        print(f"Unique movies: {dataset.unique_movies():,} \n")
        print(f"Average rating: {dataset.average_rating():.1f} \n")
        print("Top 5 highest rated movies:")
        print(dataset.top_rated_movies(), "\n")
        print("Number of movies released each year:")
        print(dataset.movies_per_year(), "\n")
        print("Number of movies in each genre:")
        print(dataset.movies_per_genre(), "\n")

        # Save dataset in JSON format        
        dataset.save_to_json(movies_json_file)

        print('Saving dataset to JSON file completed')
    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
