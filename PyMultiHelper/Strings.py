import re
from difflib import SequenceMatcher
from typing import List, Tuple


def fuzzyMatch(items: List[str],
               searchTerm: str,
               cutoff: float = 0.6) -> List[Tuple[str, float]]:
    """
    Finds fuzzy matches for a search term in a list of strings, returning the closest matches with similarity scores.

    Args:
        searchTerm (str): The term to search for in the list.
        items (List[str]): The list of strings to search within.
        cutoff (float): Minimum similarity ratio (0 to 1) required for a match to be returned. Default is 0.6.

    Returns:
        List[Tuple[str, float]]: A list of tuples, where each tuple contains a matched string and its similarity score.
                                 Results are ordered from highest to lowest similarity.
    """
    # Find the closest matches with similarity scores above the cutoff
    matches = [(match, similarityRatio(searchTerm, match)) for match in items]
    matches = [match for match in matches if match[1] >= cutoff]
    matches.sort(key=lambda x: x[1], reverse=True)

    return matches



def similarityRatio(first: str,
                    second: str) -> float:
    """
    Calculates a similarity ratio between two strings, taking into account character sequence.

    Args:
        first (str): The first string to compare.
        second (str): The second string to compare.

    Returns:
        float: A similarity ratio between 0 and 1.
    """
    return SequenceMatcher(None, first, second).ratio()


def cleanText(text: str,
              removeSpaces: bool = False,
              removePunctuation: bool = False) -> str:
    """
    Cleans the input text by removing punctuation and/or spaces, depending on the specified parameters.

    Args:
        text (str): The input text to be cleaned.
        removeSpaces (bool): If True, removes all spaces from the text. Default is False.
        removePunctuation (bool): If True, removes all punctuation from the text. Default is False.

    Returns:
        str: The cleaned text.
    """
    if removePunctuation:
        text = re.sub(r'[^\w\s]', '', text)
    if removeSpaces:
        text = text.replace(" ", "")

    return text
