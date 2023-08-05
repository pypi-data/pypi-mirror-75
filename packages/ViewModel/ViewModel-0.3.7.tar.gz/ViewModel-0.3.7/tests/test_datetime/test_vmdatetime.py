import json
from datetime import datetime
from typing import Optional

import pytest

from vmdatetime import VMDateTime, VMTimezone


class TestDateTimeZone:
    utcnow = datetime.utcnow()  # Generate once for use in parameterizing
    now = datetime.now()  # Generate once for use in parameterizing

    @pytest.mark.parametrize(
        "utc,local,timezone,timeOfDay",
        [
            [
                datetime(2020, 4, 21, 5, 34, 23, 66),
                datetime(2020, 4, 21, 17, 34, 23, 66),
                VMTimezone(offset=720, name="NZST +12", offsetDstComponent=None),
                (5 + 12) * 60 + 34  # utc +12 hours 34 minutes from midnight
            ],
            [
                datetime(2020, 4, 21, 5, 34, 23, 66),
                datetime(2020, 4, 20, 14, 34, 23, 66),
                VMTimezone(offset=-900, name="Dunno -15", offsetDstComponent=60),
                ((5 - 15) % 24) * 60 + 34  # utc - 15 hours, + 34 minutes
            ],
            [
                datetime(3000, 1, 1, 0, 0, 0, 0),
                datetime(3000, 1, 1, 0, 0, 0, 0),
                VMTimezone(offset=-0, name="GMT +0", offsetDstComponent=None),
                0
            ],
            [
                datetime(2020, 7, 21, 9, 40, 23, 66),
                datetime(2020, 7, 21, 21, 40, 23, 66),
                VMTimezone(offset=720, name="NZST +12", offsetDstComponent=60),
                (9 + 12) * 60 + 40  # utc +12 hours 40 minutes from midnight
            ],
            [
                datetime(2020, 7, 21, 9, 40, 23, 66),
                datetime(2020, 7, 21, 9, 40, 23, 66),
                None,
                (9 + 0) * 60 + 40  # utc +12 hours 40 minutes from midnight
            ]
        ]
    )
    def test_instance_from_utc_and_timezone_offset(
        self,
        utc: datetime,
        local: datetime,
        timezone: Optional[VMTimezone],
        timeOfDay: int
    ):
        dateTime = VMDateTime(utc, timezone=timezone)

        assert dateTime.utcDateTime == utc
        if dateTime.timezone:
            assert dateTime.offset == timezone.offset
            assert dateTime.timezone.offsetDstComponent is timezone.offsetDstComponent
        else:
            assert dateTime.offset == 0  # testing default value

        assert dateTime.localDateTime == local
        assert dateTime.timeOfDay == timeOfDay
        assert dateTime.dayOfWeek == local.isoweekday()
        assert dateTime.dayOfMonth == local.day
        assert dateTime.month == local.month
        assert dateTime.year == local.year

    def test_local_timezone_offset(self):
        expectedOffset = int(datetime.utcnow().astimezone().utcoffset().total_seconds() / 60)
        assert VMDateTime.calculate_local_timezone_offset() == expectedOffset

    def test_json(self):
        utc = datetime(2020, 4, 21, 5, 34, 23, 1025)  # 5:34 AM
        offset = 720  # +12 hours
        name = "NZST +12"
        offsetDstComponent = 60

        dateTime = VMDateTime(utc, timezone=VMTimezone(offset, name, offsetDstComponent))
        jsdata = dateTime.__json__()
        json_data = json.loads(jsdata)
        assert json_data["utcDateTime"] == int(utc.timestamp() * 1000)
        assert json_data["timezone"]["offset"]
        assert json_data["timezone"]["offsetDstComponent"]

    def test_now_uses_utcnow_for_time_value(self):
        vmNow = VMDateTime.now()
        now = datetime.utcnow()
        assert (now - vmNow.utcDateTime).total_seconds() < 2  # If within 1 second, most probably generated a new time

    def test_now_using_local_timezone(self):
        vmNow = VMDateTime.now(timezone=VMDateTime.localTimezone())
        expectedTimezone = datetime.utcnow().astimezone()
        assert vmNow.offset == int(expectedTimezone.utcoffset().total_seconds() / 60)
        assert vmNow.timezone.name == expectedTimezone.tzname()

    def test_now_uses_given_timezone(self):
        timezone = VMTimezone(60)
        vmNow = VMDateTime.now(timezone)
        assert vmNow.offset == timezone.offset

    def test_timezone_can_be_none(self):
        """If user does not want the local timezone or to give a timezone themselves."""
        vmNow = VMDateTime.now(timezone=None)
        assert vmNow.timezone is None
