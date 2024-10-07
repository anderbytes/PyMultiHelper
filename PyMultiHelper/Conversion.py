import csv
import os
from typing import Any
import pandas


def DICTtoCSV(data: dict, outputFile: str, separator: str = ',') -> None:
    """
    Converts a dictionary to a CSV file.

    Args:
        data (dict): The dictionary to be converted to CSV. The keys will become the header
                     and the values will be the corresponding rows in the CSV file.
        outputFile (str): The path to the output CSV file. If the file already exists, a
                          FileExistsError will be raised.
        separator (str, optional): The character that separates the values in the CSV file.
                                   Defaults to ','.

    Raises:
        FileExistsError: If the output file already exists.

    Returns:
        None: This function does not return a value. It writes the CSV data to the specified file.
    """
    if os.path.exists(outputFile):
        raise FileExistsError

    pandas.DataFrame(data).to_csv(path_or_buf=outputFile, sep=separator, index=False, doublequote=True)



def LISTtoCSV(listHeaders: list[str], listContents: list[list[Any]], outputFile: str, separator: str = ',') -> None:
    """
    Writes a list of headers and a list of content rows to a CSV file.

    Args:
        listHeaders (list[str]): A list of strings representing the headers for the CSV file.
        listContents (list[list[Any]]): A list of lists where each inner list represents a row of content
                                         corresponding to the headers.
        outputFile (str): The path to the output CSV file. If the file already exists, a
                          FileExistsError will be raised.
        separator (str, optional): The character that separates the values in the CSV file.
                                   Defaults to ','.

    Raises:
        FileExistsError: If the output file already exists.

    Returns:
        None: This function does not return a value. It writes the CSV data to the specified file.
    """
    if os.path.exists(outputFile):
        raise FileExistsError

    with open(outputFile, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=separator, doublequote=True)
        writer.writerow(listHeaders)
        writer.writerows(listContents)
