"""
Timer
"""


def time_in_seconds(
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    days: int = 0,
    weeks: int = 0,
    months: int = 0,
    years: int = 0,
) -> int:
    """
    Convert the specified time duration into a total number of `seconds`.

    Args:
        seconds (int): Number of seconds.
        minutes (int): Number of minutes.
        hours (int): Number of hours.
        days (int): Number of days.
        weeks (int): Number of weeks.
        months (int): Number of months (approximated as 30 days per month).
        years (int): Number of years (approximated as 365 days per year).

    Returns:
        int: Total time duration in seconds.
    """

    # Convert each time unit to seconds and sum them up
    total_seconds = (
        seconds
        + minutes * 60
        + hours * 3600
        + days * 86400
        + weeks * 604800
        + months * 2592000  # Approximation: 30 days per month
        + years * 31536000  # Approximation: 365 days per year
    )

    return total_seconds
