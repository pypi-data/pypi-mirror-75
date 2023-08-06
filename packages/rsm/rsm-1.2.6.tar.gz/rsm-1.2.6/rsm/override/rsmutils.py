from datetime import datetime

from rsm.handlers.logging import LogHandler
from rsm.utils import misc
from rsm.utils import time

debug = LogHandler().logger.debug


class RsmUtils:
    """ Replace the original SiemplifyUtils """
    def __init__(self):
        debug('Initializing class `RsmUtils` to override methods from `SiemplifyUtils`')

    @staticmethod
    def convert_string_to_unix_time(dt_str: str) -> int:
        return time.convert_string_to_unix_time(dt_str)

    @staticmethod
    def convert_datetime_to_unix_time(dt: datetime) -> int:
        return time.convert_datetime_to_unix_time(dt, True)

    @staticmethod
    def convert_unixtime_to_datetime(epoch: int) -> datetime:
        return time.convert_unixtime_to_datetime(epoch)

    @staticmethod
    def convert_string_to_datetime(dt_str, tz=None) -> datetime:
        return time.convert_string_to_datetime(dt_str)

    @staticmethod
    def validate_timestamp(last_run_timestamp: datetime, offset: int = 0) -> datetime:
        return time.validate_timestamp(last_run_timestamp, offset)

    @staticmethod
    def dict_to_flat(d: dict) -> dict:
        """ Replace the original method `dict_to_flat` to wrap `flatten` method. """
        return misc.dict_to_flat(d)