import random


def commonElements(list1: list,
                   list2: list) -> list:
    """
    Returns a list of common elements between two lists.

    Args:
        list1 (list): The first list of elements.
        list2 (list): The second list of elements.

    Returns:
        list: A list containing elements that are common to both lists.
    """
    return list(set(list1) & set(list2))

def chunkList(inputList: list,
               chunkSize: int) -> list[list]:
    """
    Splits a list into smaller chunks of specified size.

    Args:
        inputList (list): The list to be chunked.
        chunkSize (int): The size of each chunk.

    Returns:
        list[list]: A list containing the chunks.
    """
    return [inputList[i:i + chunkSize] for i in range(0, len(inputList), chunkSize)]

def findDuplicates(inputList: list) -> list:
    """
    Identifies and returns duplicates in a list.

    Args:
        inputList (list): The list to check for duplicates.

    Returns:
        list: A list of duplicates found in the input list.
    """
    seen = set()
    duplicates = set()
    for item in inputList:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


def shuffleList(inputList: list) -> list:
    """
    Shuffles the elements of a list randomly.

    Args:
        inputList (list): The list to be shuffled.

    Returns:
        list: The shuffled list.
    """
    shuffledList = inputList[:]
    random.shuffle(shuffledList)
    return shuffledList