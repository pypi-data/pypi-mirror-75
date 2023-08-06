from datetime import datetime, timedelta
from rsm.override.rsmsdk import RsmSDK
from rsm.handlers.logging import LogHandler
from dateutil import parser
import pytz
import os

TIMESTAMP_FILE = "timestamp.stmp"
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
utc = pytz.timezone('UTC')
eastern = pytz.timezone('US/Eastern')

log = LogHandler()
debug = log.logger.debug
info = log.logger.info
error = log.logger.error

# HELP YOURSELF BY READING THIS.
#
# There is only one unix time and it is created by using UTC/GMT time zone.
# This means time should always be handled by timestamps and can be presented in human readable format
# but it will only be converted for this purpose.
#
# In short, any logic should use timestamps.


# The preferred way of dealing with times is to always work in UTC,
# converting to localtime only when generating output to be read by humans.

# >>> utc_dt = datetime(2002, 10, 27, 6, 0, 0, tzinfo=utc)
# >>> loc_dt = utc_dt.astimezone(eastern)
# >>> loc_dt.strftime(fmt)
# '2002-10-27 01:00:00 EST-0500'

# Creating local times is also tricky, and the reason why working with local times is not recommended.
# Unfortunately, you cannot just pass a tzinfo argument when constructing a datetime

# source: http://pytz.sourceforge.net/


def convert_datetime_to_unix_time(dt: datetime, ms=True) -> int:
    """
    returns the time in unix time
    :param ms:
    :param dt: {datetime}
    :return: {unix time}
    """
    return int(dt.timestamp()) * 1000 if ms else int(dt.timestamp())


def from_utc_to_timezone(time: datetime or str or int, timezone: pytz.timezone = None) \
        -> datetime or int or str:
    """

    :param time: UTC time
    :param timezone: timezone to convert time to
    :return: converted datetime
    """

    timezone = pytz.timezone(timezone)
    if isinstance(time, str):
        debug('Variable `time` is type < str >, removing tzinfo and parsing datetime')
        time = parser.parse(time).timestamp()

    if isinstance(time, (int, float)):
        debug('Variable `time` is type < int >, removing tzinfo and parsing datetime')
        if isinstance(time, float):
            time = int(time)

        try:
            if len(str(int(time))) == 10:  # timestamp in seconds
                time = time * 1000

            return datetime.fromtimestamp(int(time.timestamp())).astimezone(timezone)
        except OverflowError as err:
            error(err)

    # Converting to localtime ONLY when generating output to be read by humans.
    return time.astimezone(timezone)


def convert_string_to_datetime(datetime_str: str) \
        -> datetime:
    """
    returns time in datetime format
    """
    try:

        # This does NOT convert timezone, it defines the TIMEZONE of this datetime.
        # Example:
        #
        # >>> dt = 2020-05-05 00:00:00+00:00
        # >>> timezone = pytz.timezone("US/Eastern")
        # >>> dt = dt.astimezone(timezone)
        #
        # returns ---> 2020-05-05 00:00:00-04:00

        return parser.parse(datetime_str)

    except Exception as e:
        raise Exception(
            "{0}: {1}".format(
                "convert_string_to_datetime Failed",
                str(e)))  # TODO: Why raise again?


def convert_unixtime_to_datetime(unix_time: int) -> datetime:
    """
    returns the time in local time with stated TZ
    """
    try:
        return datetime.fromtimestamp(unix_time)
    except Exception as e:
        raise Exception(
            "{0}: {1}".format(
                "convert_unixtime_to_datetime Failed",
                str(e)))  # TODO: Why raise again?


def convert_string_to_unix_time(datetime_str: str = None) -> int:
    """
    return time in unix time format
    """
    try:
        dt = convert_string_to_datetime(datetime_str)
        return convert_datetime_to_unix_time(dt, True)
    except Exception as e:
        raise Exception(
            "{0}: {1}".format(
                "convert_string_to_unix_time Failed",
                str(e)))  # TODO: Why raise again?


def validate_timestamp(last_run_timestamp: datetime, offset: int) -> datetime:
    """
    Validate timestamp in range
    """

    if isinstance(last_run_timestamp, str):
        last_run_timestamp = datetime.strptime(last_run_timestamp, fmt)

    current_time = datetime.utcnow()
    if current_time - last_run_timestamp < timedelta(days=offset):
        return current_time - timedelta(days=offset)
    else:
        return last_run_timestamp


def fetch_timestamp(datetime_format=False):
    """
    get timestamp
    :param datetime_format: {boolean} if datetime - return timestamp as datetime
    :return: {unix time/ datetime}
    """
    rsm_sdk_config = RsmSDK()
    save_file_path = os.path.join(rsm_sdk_config.run_folder_path, TIMESTAMP_FILE)

    last_run_time = 0
    if os.path.isfile(save_file_path):
        with open(save_file_path, 'r') as f:
            last_run_time = f.read()
            f.close()

    try:
        last_run_time = int(last_run_time)
    except BaseException:
        last_run_time = convert_string_to_unix_time(last_run_time)

    if datetime_format:
        last_run_time = convert_unixtime_to_datetime(last_run_time)

    else:
        last_run_time = int(last_run_time)

    return last_run_time
