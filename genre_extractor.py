import ast
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenreExtractor:
    """A class to extract genre from genres data."""

    @staticmethod
    def extract_genre(genres_data):
        """
        Extract the genre name from the genre data.

        :param genre_data: A string representation of a list of dictionaries containing genres information .
        :return: The genre or None if not found.
        """
        try:            
            genres_list = ast.literal_eval(str(genres_data))
            return [genre['name'] for genre in genres_list]

        except ValueError as e:
            logger.error(f"Invalid input: {e}")
            return []

        except SyntaxError as e:
            logger.error(f"Invalid input: {e}")
            return []

        except Exception as e:
            logger.error(f"Genre extraction failed: {e}")
            raise
