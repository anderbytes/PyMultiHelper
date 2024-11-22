import csv
import os

from pandas import DataFrame
from typing import Any, Dict, List, Union


def DICTtoCSV(data: Union[Dict[str, List[Any]], List[Dict[str, Any]]], outputFile: str, separator: str = ',') -> None:
    """
    Converts a dictionary or a list of dictionaries to a CSV file, with input validation for each case.

    Args:
        data (Union[Dict[str, List[Any]], List[Dict[str, Any]]]): The data to be converted to CSV.
            - If a dictionary is provided, the keys should represent column headers and each value should be a list.
            - If a list of dictionaries is provided, each dictionary should represent a row of data with consistent keys.
        outputFile (str): The path to the output CSV file. If the file already exists, a FileExistsError will be raised.
        separator (str, optional): The character that separates the values in the CSV file. Defaults to ','.

    Raises:
        FileExistsError: If the output file already exists.
        TypeError: If 'data' is not a dictionary or a list of dictionaries, or if 'separator' is not a single character.
        ValueError: If 'outputFile' does not end with '.csv', or if 'data' is empty or has incompatible values.

    Returns:
        None: This function does not return a value. It writes the CSV data to the specified file.

    Examples:
        Valid Usage with Dictionary of Lists:
        >>> people = {
        >>>  "Name": ["Alice", "Bob", "Charlie"],
        >>>  "Age": [24, 30, 35],
        >>>  "City": ["New York", "Los Angeles", "Chicago"]
        >>>  }

        Valid Usage with List of Dictionaries:
         >>> people = [
         >>>  {"Name": "Alice", "Age": 24, "City": "New York"},
         >>>  {"Name": "Bob", "Age": 30, "City": "Los Angeles"},
         >>>  {"Name": "Charlie", "Age": 35, "City": "Chicago"}
         >>> ]

        Invalid Usage 1 (causes ValueError due to inconsistent keys in list of dictionaries):
        >>> people = [
        >>>  {"Name": "Alice", "Age": 24},
        >>>  {"Name": "Bob", "Age": 30, "City": "Los Angeles"},  # Missing "City" in first item
        >>>  {"Name": "Charlie", "City": "Chicago"}  # Missing "Age"
        >>>  ]
        # Explanation: Each dictionary in 'data' must have the same keys to ensure consistent columns in the CSV.

        Invalid Usage 2 (causes ValueError due to non-list values in dictionary):
        >>> people = {
        >>>  "Name": "Alice",
        >>>  "Age": 24,
        >>>  "City": "New York"
        >>>  }
        # Explanation: The 'data' dictionary expects each value to be a list representing a column of entries.
        # In this case, the values are single items (str and int), which cannot be written to CSV as columns.

        >>> DICTtoCSV(data, "output.csv")
    """
    # Validate 'outputFile' extension and 'separator' type
    if not isinstance(outputFile, str) or not outputFile.endswith('.csv'):
        raise ValueError("The 'outputFile' must be a string with a '.csv' extension.")
    if not isinstance(separator, str) or len(separator) != 1:
        raise TypeError("The 'separator' must be a single character string.")
    if os.path.exists(outputFile):
        raise FileExistsError(f"The file '{outputFile}' already exists. Please choose a different filename.")

    # Convert list of dictionaries to a DataFrame if needed
    if isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            data = DataFrame(data)  # Convert list of dicts to DataFrame
        else:
            raise TypeError("If 'data' is a list, each element must be a dictionary with the same keys.")
    elif isinstance(data, dict):
        if all(isinstance(value, list) for value in data.values()):
            data = DataFrame(data)  # Convert dict of lists to DataFrame
        else:
            raise ValueError("If 'data' is a dictionary, each value must be a list corresponding to a column.")
    else:
        raise TypeError("The 'data' argument must be either a dictionary of lists or a list of dictionaries.")

    # Write the DataFrame to a CSV file
    data.to_csv(path_or_buf=outputFile, sep=separator, index=False, doublequote=True)



def LISTtoCSV(listHeaders: List[str], listContents: List[List[Any]], outputFile: str, separator: str = ',') -> None:
    """
    Writes a list of headers and a list of content rows to a CSV file with additional input validations.

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
        TypeError: If listHeaders or separator are not of the expected types.
        ValueError: If listHeaders or listContents have incompatible lengths or are empty, or if
                    outputFile does not end in .csv.

    Returns:
        None: This function does not return a value. It writes the CSV data to the specified file.
    """
    # Validate listHeaders is a list of strings
    if not isinstance(listHeaders, list) or not all(isinstance(header, str) for header in listHeaders):
        raise TypeError("The 'listHeaders' must be a list of strings.")

    # Validate listContents is a list of lists with correct row lengths
    if not isinstance(listContents, list) or not all(isinstance(row, list) for row in listContents):
        raise TypeError("The 'listContents' must be a list of lists.")
    if any(len(row) != len(listHeaders) for row in listContents):
        raise ValueError("Each row in 'listContents' must have the same number of elements as 'listHeaders'.")

    # Ensure listHeaders and listContents are not empty
    if not listHeaders:
        raise ValueError("The 'listHeaders' list cannot be empty.")
    if not listContents:
        raise ValueError("The 'listContents' list cannot be empty.")

    # Check if outputFile is a string and ends with '.csv'
    if not isinstance(outputFile, str) or not outputFile.endswith('.csv'):
        raise ValueError("The 'outputFile' must be a string with a '.csv' extension.")

    # Check if separator is a single character
    if not isinstance(separator, str) or len(separator) != 1:
        raise TypeError("The 'separator' must be a single character string.")

    # Check if the output file already exists
    if os.path.exists(outputFile):
        raise FileExistsError(f"The file '{outputFile}' already exists. Please choose a different filename.")

    # Write to the CSV file if all checks pass
    with open(outputFile, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=separator, doublequote=True)
        writer.writerow(listHeaders)
        writer.writerows(listContents)


def OBJLISTtoCSV(data: List[Any], outputFile: str, separator: str = ',') -> None:
    """
    Converts a list of objects to a CSV file. The object's attributes become the column headers.

    Args:
        data (List[Any]): A list of objects (e.g., instances of a class) to be converted to CSV.
                          Each object's attributes will form the columns.
        outputFile (str): The path to the output CSV file. If the file already exists, a
                          FileExistsError will be raised.
        separator (str, optional): The character that separates the values in the CSV file.
                                   Defaults to ','.

    Raises:
        FileExistsError: If the output file already exists.
        ValueError: If 'outputFile' does not end with '.csv' or if 'data' is empty.
        TypeError: If 'separator' is not a single character.

    Returns:
        None: This function does not return a value. It writes the CSV data to the specified file.
    """

    # Validate 'outputFile' and 'separator'
    if not isinstance(outputFile, str) or not outputFile.endswith('.csv'):
        raise ValueError("The 'outputFile' must be a string with a '.csv' extension.")
    if not isinstance(separator, str) or len(separator) != 1:
        raise TypeError("The 'separator' must be a single character string.")
    if os.path.exists(outputFile):
        raise FileExistsError(f"The file '{outputFile}' already exists. Please choose a different filename.")

    # Validate 'data' and infer field names from the first object
    if not data:
        raise ValueError("The 'data' list cannot be empty.")

    first_obj = data[0]

    # Get field names in the order they are defined in the object
    field_names = list(vars(first_obj).keys())

    # Prepare rows from object attributes
    rows = []
    for obj in data:
        row = {field: getattr(obj, field, None) for field in field_names}
        rows.append(row)

    # Write data to CSV
    with open(outputFile, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names, delimiter=separator)
        writer.writeheader()
        writer.writerows(rows)


def chunksProcess(
        items: list,
        chunkSize: int,
        function: callable
):
    """
    Processes a list of items in chunks, applying a callback to each chunk.

    Args:
        items (list): The list of items to be processed.
        chunkSize (int): The maximum size of each chunk.
        function (callable): The function to be applied to each chunk.
                             It should accept a list as its only parameter.

    Raises:
        ValueError: If chunkSize is less than or equal to zero.
    """

    if chunkSize <= 0:
        raise ValueError("chunkSize must be greater than zero.")

    for i in range(0, len(items), chunkSize):
        chunk = items[i:i + chunkSize]
        function(chunk)