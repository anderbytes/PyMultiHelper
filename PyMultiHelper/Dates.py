from datetime import datetime, timedelta, timezone, date
from typing import Optional, List

import pytz
import re


def dateRanges(startDate: str,
               endDate: str,
               rangeSize: int = 30):
    """
        Returns a list of date ranges of 'rangeSize' days between start and end date.
        Useful for:
         - Repeating API calls that use a 'Days Limit' for each range called

        Args:
            rangeSize (int): Max number of days in each resulting range
            startDate (str): The start date of the total range
            endDate (str): The end date of the total range

        Returns:
            list(str, str): List of one or more date ranges, each one with the max specified range size.

        Examples:
            >>> dateRanges("2020-02-25", "2020-08-24", 90)
        """

    ranges = []

    # Convert date strings to datetime objects
    inicio = datetime.strptime(startDate, '%Y-%m-%d')
    fim = datetime.strptime(endDate, '%Y-%m-%d')

    # Define an interval
    one_month = timedelta(days=rangeSize)

    # Define the current date as the starting date
    data_atual = inicio

    # Loop while the current date is lesser or equal the final date
    while data_atual <= fim:
        # Define the start and end date of the current interval
        inicio_intervalo = data_atual
        fim_intervalo = min(data_atual + one_month - timedelta(days=1), fim)

        # Add the interval to the ranges list
        ranges.append((inicio_intervalo.strftime('%Y-%m-%d'), fim_intervalo.strftime('%Y-%m-%d')))

        # Add a month to the current date
        data_atual += one_month

    # Return the ranges list
    return ranges


def STRtoDATETIME(dateString: str) -> datetime:
    """
    Transforms a datetime string into a datetime object.

    Args:
        dateString (str): A datetime string, which can be in various formats, e.g.
                     '2022-08-01T12:53:40.000Z' or '2022-08-01 12:53:40+00:00'.

    Returns:
        datetime: A datetime object corresponding to the provided string.

    Raises:
        ValueError: If the provided string is not a valid datetime format.
    """
    # Regular expression to validate datetime formats
    pattern = r'^\d{4}[-/]\d{2}[-/]\d{2}(?:[ T]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)?$'

    if not re.match(pattern, dateString):
        raise ValueError(f"The provided string '{dateString}' is not a valid datetime format.")

    # Normalize the string to ensure it has a timezone
    if 'Z' in dateString:
        isoformat_str = dateString.replace('Z', '+00:00')
    else:
        isoformat_str = dateString

    return datetime.fromisoformat(isoformat_str)


def DATETIMEtoSTR(originalDate: datetime,
                  tzString: str = 'UTC') -> str:
    """
    Transforms a datetime object to a string of format 'YYYY-MM-DDTHH:MM:SS+00:00'.

    Args:
        originalDate (datetime): The datetime object to be converted.
        tzString (str): The timezone to convert the datetime to (default is 'UTC').
                            Can be a valid timezone name (e.g., 'America/New_York')
                            or an offset string (e.g., '-03:00').

    Returns:
        str: String representation of the datetime in the specified timezone.

    Raises:
        ValueError: If the tzString is not a valid timezone or offset.
    """
    # Validate the timezone_str
    try:
        # Check if timezone_str is a valid offset
        if tzString.startswith('-') or tzString.startswith('+'):
            offset_hours, offset_minutes = map(int, tzString[1:].split(':'))
            offset = timedelta(hours=offset_hours, minutes=offset_minutes)
            tz = timezone(offset if tzString.startswith('+') else -offset)
        else:
            # Assume it's a timezone name
            tz = pytz.timezone(tzString)
    except (pytz.UnknownTimeZoneError, ValueError):
        raise ValueError(
            f"The provided timezone '{tzString}' is not valid. Please provide a valid timezone or offset.")

    # Convert to the specified timezone
    originalDate = originalDate.astimezone(tz)

    # Return the ISO format string
    return originalDate.isoformat(timespec='seconds')


def businessDaysBetween(startDate: date,
                        endDate: date,
                        holidays: Optional[List[date]] = None,
                        includeStart: bool = True,
                        includeEnd: bool = True) -> int:
    """
    Calculates the number of business days between two dates, excluding weekends and optional holidays.
    Allows excluding the start and/or end dates from the count.

    Args:
        startDate (date): The start date of the range.
        endDate (date): The end date of the range.
        holidays (Optional[List[date]]): A list of holiday dates to exclude from the count. Defaults to None.
        includeStart (bool): If True, includes the start date in the count. Defaults to True.
        includeEnd (bool): If True, includes the end date in the count. Defaults to True.

    Returns:
        int: The number of business days between startDate and endDate.
    """
    # Define set for holidays if provided
    holidays = set(holidays) if holidays else set()

    # Adjust start and end dates based on include_start and include_end flags
    if not includeStart:
        startDate += timedelta(days=1)
    if not includeEnd:
        endDate -= timedelta(days=1)

    # Initialize count and iterate over date range
    business_days_count = 0
    current_date = startDate

    while current_date <= endDate:
        if current_date.weekday() < 5 and current_date not in holidays:
            business_days_count += 1
        current_date += timedelta(days=1)

    return business_days_count

def calculateAge(birthDate: date) -> int:
    """
    Calculates the age based on the provided birth date.

    Args:
        birthDate (date): The birth date.

    Returns:
        int: The calculated age.
    """
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age

def hoursMinsAgo(sourceDateTime: datetime, hoursAgoText: str = "hours ago", minutesAgoText: str = "minutes ago") -> str:
    """
    Returns a human-readable time difference in either hours or minutes
    between the current time and the provided datetime.

    Args:
        sourceDateTime (datetime): The datetime to compare to the current time.
        hoursAgoText (str): The text showed as 'hours ago' template
        minutesAgoText (str): The text showed as 'minutes ago' template

    Returns:
        str: A string indicating the time difference in hours or minutes (e.g., "5 hours ago" or "30 minutes ago").
    """
    delta_seconds = int((datetime.now() - sourceDateTime).total_seconds())
    hours = delta_seconds // 3600
    if hours > 0:
        return f"{hours} {hoursAgoText}"
    else:
        minutes = delta_seconds // 60
        return f"{minutes} {minutesAgoText}"