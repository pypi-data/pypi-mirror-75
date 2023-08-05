from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple

from objdict import dumps, to_json


@to_json()
@dataclass
class VMTimezone:
    offset: int
    name: str = ""
    offsetDstComponent: Optional[int] = None


@dataclass
class VMDateTime:
    """
    A complete datetime and timezone solution for storing datetime values without losing timezone
    information.
    """
    utcDateTime: datetime
    timezone: Optional[VMTimezone]

    def __json__(self, internal: bool = False, forDatabase: bool = False):
        """
        :param internal: Output a JSON str if true, otherwise is being used for "internal" ObjDict dumps work.
        :param forDatabase: Special case for saving to the database, adding addtional computed values
            that enable better querying.
        :return: A JSON string or dict depending on internal
        """

        def exclude_nulls(attrs: List[Tuple[str, Any]]):
            return {key: value for key, value in attrs if value}

        data = asdict(self, dict_factory=exclude_nulls)
        if forDatabase:
            data["localisedFilters"] = {
                "timeOfDay": self.timeOfDay,
                "dayOfWeek": self.dayOfWeek,
                "dayOfMonth": self.dayOfMonth,
                "month": self.month,
                "year": self.year
            }
        else:
            tsInMilliseconds = int(self.utcDateTime.timestamp() * 1000)  # convert to milliseconds
            data["utcDateTime"] = tsInMilliseconds  # encode datetime as int of timestamp in milliseconds for json
        if internal:
            return data

        return dumps(data)

    @staticmethod
    def now(timezone: VMTimezone = None):
        """
        Generate a new VMDateTime with the current time and timezone. Timezone defaulting to local machine if
        not provided.
        """
        return VMDateTime(datetime.utcnow(), timezone)

    @staticmethod
    def localTimezone() -> VMTimezone:
        localTimezone = datetime.utcnow().astimezone()
        offset = VMDateTime.calculate_local_timezone_offset(localTimezone)
        return VMTimezone(offset, localTimezone.tzname())

    @property
    def offset(self) -> int:
        if self.timezone:
            return self.timezone.offset
        else:
            return 0

    @property
    def timeOfDay(self) -> int:
        """Local time in minutes since 00:00 (midnight)"""
        return self.localDateTime.hour * 60 + self.localDateTime.minute

    @property
    def dayOfWeek(self) -> int:
        """
        Day of the week in local time according to ISO standards for
        representing the day of the week as an int. 1-7:Monday-Sunday.
        """
        return self.localDateTime.isoweekday()

    @property
    def dayOfMonth(self) -> int:
        return self.localDateTime.day

    @property
    def month(self) -> int:
        return self.localDateTime.month

    @property
    def year(self) -> int:
        return self.localDateTime.year

    @property
    def offsetTimeDelta(self) -> timedelta:
        return timedelta(minutes=self.offset)

    @property
    def localDateTime(self) -> datetime:
        return self.utcDateTime + self.offsetTimeDelta

    @staticmethod
    def calculate_local_timezone_offset(local_zone=None) -> int:
        """A naive implementation to get the local timezone offset of the machine."""
        if not local_zone:
            local_zone = datetime.utcnow().astimezone()
        return int(local_zone.utcoffset().total_seconds() / 60)
