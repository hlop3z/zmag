"""
This module provides a utility to create date, time and datetime values.
"""

import datetime as dt
from typing import Any


class Date:
    """DateTime (UTC)"""

    utc_timezone = dt.timezone.utc

    @classmethod
    def datetime(cls) -> Any:
        """DateTime (UTC)"""
        return dt.datetime.now(cls.utc_timezone)

    @classmethod
    def date(cls) -> Any:
        """Date (UTC)"""
        return dt.datetime.now(cls.utc_timezone).date()

    @classmethod
    def time(cls) -> Any:
        """Time (UTC)"""
        return dt.datetime.now(cls.utc_timezone).time()
