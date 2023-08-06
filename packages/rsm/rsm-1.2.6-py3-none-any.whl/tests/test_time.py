from unittest import TestCase
from datetime import datetime
from rsm.utils import time

datetime = datetime.now()
datetime_str = "2020-06-17 23:00:00"


class TestTime(TestCase):
    def test_change_datetime_timezone_datetime(self):
        assert (type(time.from_utc_to_timezone(datetime, timezone="US/Eastern")))

    def test_change_datetime_timezone_string(self):
        assert (time.from_utc_to_timezone(datetime_str, timezone="US/Eastern"))

    def test_change_datetime_timezone_timestamp(self):
        assert time.from_utc_to_timezone(datetime.timestamp(), timezone="Europe/Amsterdam")

    def test_convert_datetime_to_unix_time(self):
        result = time.convert_datetime_to_unix_time(datetime, True)
        print(result)
        assert result

    def test_convert_string_to_datetime(self):
        result = time.convert_string_to_datetime(datetime_str)
        print(result)
        assert result

    def test_convert_unixtime_to_datetime(self):
        result = time.convert_unixtime_to_datetime(datetime.timestamp())
        print(result)
        assert result

    def test_convert_string_to_unix_time(self):
        result = time.convert_string_to_unix_time(datetime_str)
        print(result)
        assert result

    def test_validate_timestamp(self):
        result = time.validate_timestamp(datetime, offset=0)
        print(result)
        assert result


