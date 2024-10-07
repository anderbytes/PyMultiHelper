import re
from datetime import datetime


def validateEmail(email: str) -> bool:
    """
    Validates an email string based on common criteria.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email is valid, False otherwise.

    Raises:
        ValueError: If the input is not a string.
    """

    # Email Regex (critical validation)
    # Explanation:
    # - Begins with alphanumeric characters or certain special characters (-, _, .)
    # - A single '@' symbol
    # - Domain name with at least one period
    # - Ends with a valid domain suffix (2-4 characters)

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,4}$'

    # Match the regex against the provided email
    return re.match(email_regex, email) is not None


def validateDateFormat(dateString: str, dateFormat: str) -> bool:
    """
    Validates if the given date string matches the provided date/time formats.

    Args:
        dateString (str): The date (or date/time) string to validate.
        dateFormat (str): The format that the date string should match.
                           This should be written following the patterns used
                           in the Python `strptime`/`strftime` methods, which are based on
                           standard C date formatting directives.
                           Some common format codes include:
                               - %Y: Year (4 digits)
                               - %m: Month (2 digits, zero-padded)
                               - %d: Day of the month (2 digits, zero-padded)
                               - %H: Hour (24-hour clock, 2 digits, zero-padded)
                               - %M: Minute (2 digits, zero-padded)
                               - %S: Second (2 digits, zero-padded)
                               - %z: UTC offset in the form +HHMM or -HHMM
                               - %Z: Time zone name
                               - %p: AM/PM

                           Example: '%Y-%m-%d %H:%M:%S' corresponds to '2023-09-29 15:45:00'.

    Returns:
        bool: True if the date string matches the date format, False otherwise.

    Raises:
        ValueError: If the date format is invalid or not recognized.
    """
    try:
        # Try to parse the date string with the provided format
        datetime.strptime(dateString, dateFormat)
        return True
    except ValueError:
        # If parsing fails, it raises a ValueError and returns False
        return False

def validateAnyDate(dateString: str) -> bool:
    """
    Validates a date string in multiple formats (e.g., DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD),
    accepting day-month-year, month-day-year, and year-month-day permutations.
    The function supports `/`, `-`, and `.` as date separators, but does not allow mixed separators in the same string.

    Args:
        dateString (str): The date string to be validated.

    Returns:
        bool: True if the date is valid, False otherwise.

    """

    # Define regex patterns for consistent separators in date formats
    date_patterns = [
        # DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY (all separators must be the same)
        r'^(0[1-9]|[12][0-9]|3[01])([\/\-\.])(0[1-9]|1[0-2])\2(\d{4})$',

        # MM/DD/YYYY, MM-DD-YYYY, MM.DD.YYYY
        r'^(0[1-9]|1[0-2])([\/\-\.])(0[1-9]|[12][0-9]|3[01])\2(\d{4})$',

        # YYYY/MM/DD, YYYY-MM-DD, YYYY.MM.DD
        r'^(\d{4})([\/\-\.])(0[1-9]|1[0-2])\2(0[1-9]|[12][0-9]|3[01])$',

        # DD/MM/YY, DD-MM-YY, DD.MM.YY
        r'^(0[1-9]|[12][0-9]|3[01])([\/\-\.])(0[1-9]|1[0-2])\2(\d{2})$',

        # MM/DD/YY, MM-DD-YY, MM.DD.YY
        r'^(0[1-9]|1[0-2])([\/\-\.])(0[1-9]|[12][0-9]|3[01])\2(\d{2})$',

        # YY/MM/DD, YY-MM-DD, YY.MM.DD
        r'^(\d{2})([\/\-\.])(0[1-9]|1[0-2])\2(0[1-9]|[12][0-9]|3[01])$'
    ]

    # Iterate over all patterns to check for a match
    for pattern in date_patterns:
        if re.match(pattern, dateString):
            return True

    return False


def validateDate_8601(dateString: str) -> bool:
    """
    Validates a date string in the format YYYY-MM-DD (ISO 8601) only, accepting `/`, `-`, or `.` as separators.
    The separators must be consistent throughout the string.

    Args:
        dateString (str): The date string to be validated.

    Returns:
        bool: True if the date is valid, False otherwise.

    """

    # Regex pattern for YYYY-MM-DD, YYYY/MM/DD, or YYYY.MM.DD
    pattern = r'^(\d{4})([\/\-\.])(0[1-9]|1[0-2])\2(0[1-9]|[12][0-9]|3[01])$'

    # Match against the pattern
    if re.match(pattern, dateString):
        return True

    return False


def validateYear(year: int, minYear: int = 1900, maxYear: int = 2199) -> bool:
    """
    Validates if the given year is within the specified range.

    :param year: The year to be validated.
    :param minYear: The minimum valid year (inclusive). Default is 1900.
    :param maxYear: The maximum valid year (inclusive). Default is 2199.
    :return: True if the year is valid, False otherwise.

    Example:
    >>> validateYear(2023)
    True
    >>> validateYear(1800)
    False
    """
    return minYear <= year <= maxYear


def matchesRegex(string: str, regex: str) -> bool:
    """
    Checks if a string contains a specified regular expression pattern.

    Args:
        string (str): The string to be checked.
        regex (str): The regular expression pattern to be searched in the string.

    Returns:
        bool: True if the regex pattern is found in the string, False otherwise.
    """

    # Compile the regular expression pattern
    pattern = re.compile(regex)

    # Search for the regex pattern in the string
    return bool(pattern.search(string))