import ast
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DirectorExtractor:
    """A class to extract director name from crew data."""

    @staticmethod
    def extract_director(crew_data: str) -> str:
        """
        Extract the director's name from the crew data.

        :param crew_data: A string representation of a list of dictionaries containing crew information.
        :return: The director's name or None if not found.
        """
        try:
            crew_list = ast.literal_eval(crew_data)
            if not isinstance(crew_list, list):
                logger.error("Crew data must be a list")
                return []

            for crew_member in crew_list:
                if not isinstance(crew_member, dict):
                    logger.error("Crew member data must be a dictionary")
                    return []
                if crew_member["job"] == "Director":
                    return crew_member["name"]
            return None
        
        except ValueError as e:
            logger.error(f"Invalid input: {e}")
            return []

        except SyntaxError as e:
            logger.error(f"Invalid input: {e}")
            return []

        except Exception as e:
            logger.error(f"Genre extraction failed: {e}")
            raise
