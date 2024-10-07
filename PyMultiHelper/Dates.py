from datetime import datetime, timedelta, timezone
import pytz
import re


def dateRanges(startDate: str, endDate: str, rangeSize: int = 30):
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

    # Converte as strings de data em objetos datetime
    inicio = datetime.strptime(startDate, '%Y-%m-%d')
    fim = datetime.strptime(endDate, '%Y-%m-%d')

    # Define um intervalo
    one_month = timedelta(days=rangeSize)

    # Define a data atual como a data de início
    data_atual = inicio

    # Inicializa a lista de ranges
    ranges = []

    # Loop enquanto a data atual for menor ou igual à data final
    while data_atual <= fim:
        # Define a data de início e fim do intervalo atual
        inicio_intervalo = data_atual
        fim_intervalo = min(data_atual + one_month - timedelta(days=1), fim)

        # Adiciona o intervalo à lista de ranges
        ranges.append((inicio_intervalo.strftime('%Y-%m-%d'), fim_intervalo.strftime('%Y-%m-%d')))

        # Adiciona um mês à data atual
        data_atual += one_month

    # Retorna a lista de ranges
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


def DATETIMEtoSTR(date: datetime, tzString: str = 'UTC') -> str:
    """
    Transforms a datetime object to a string of format 'YYYY-MM-DDTHH:MM:SS+00:00'.

    Args:
        date (datetime): The datetime object to be converted.
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
    date = date.astimezone(tz)

    # Return the ISO format string
    return date.isoformat(timespec='seconds')
