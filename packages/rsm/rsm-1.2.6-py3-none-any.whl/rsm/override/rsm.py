from rsm.handlers.logging import LogHandler
from rsm.override.rsmutils import RsmUtils
from rsm.override.rsmsdk import RsmSDK
from datetime import datetime
import os

log = LogHandler()
debug = log.logger.debug
info = log.logger.info
error = log.logger.error

# Override the method `override_stdout` to be able to print in console.
# (Line 11, SiemplifyConnectors.py)
try:
    import SiemplifyUtils

    def _override_stdout():
        pass

    debug('Overriding method `override_stdout` with `_override_stdout`')
    SiemplifyUtils.override_stdout = _override_stdout
    SiemplifyUtils.convert_string_to_unix_time = RsmUtils.convert_string_to_unix_time
    SiemplifyUtils.convert_unixtime_to_datetime = RsmUtils.convert_unixtime_to_datetime
    SiemplifyUtils.convert_datetime_to_unix_time = RsmUtils.convert_datetime_to_unix_time
    SiemplifyUtils.convert_string_to_datetime = RsmUtils.convert_string_to_datetime
    SiemplifyUtils.dict_to_flat = RsmUtils.dict_to_flat
    # End of override, next we are importing the module and it will use the
    # override method instead of the original.
    debug('Importing module `SiemplifyBase` after overriding method')
    from SiemplifyConnectors import SiemplifyConnectorExecution  # E402

except ModuleNotFoundError as err:
    error(err)
except ImportError as err:
    error(err)


class RsmBase(SiemplifyConnectorExecution):
    def __init__(self):
        debug('Initializing class `RsmBase` with inheritance of `SiemplifyBase`')
        self.sdk_config = RsmSDK()

        # Fix: AttributeError: 'SiemplifyBase' object has no attribute
        # 'run_folder_path' (Line 13 SiemplifyBase.py)
        self.run_folder_path = self.sdk_config.run_folder_path

        info(f"'run_folder_path' = '{self.sdk_config.run_folder_path}'")
        debug('Supercharging `RsmBase`!')

        super(RsmBase, self).__init__()
        self.now = int(datetime.now().timestamp()) * 1000

    def save_timestamp(self, **kwargs):
        """
        save timestamp

        """
        new_timestamp = kwargs.get('new_timestamp', None)
        save_file_path = os.path.join(self.run_folder, self.TIMESTAMP)

        try:
            with open(save_file_path, 'w') as time_file:
                if isinstance(new_timestamp, (int, float)):
                    if len(str(int(new_timestamp))
                           ) == 10:  # timestamp in seconds
                        new_timestamp = new_timestamp * 1000
                    self.now = int(new_timestamp)
                elif new_timestamp is not None:
                    raise TypeError("new_timestamp must be in epoch time")
                time_file.write(str(self.now))
                time_file.close()

                return True
        except Exception as err:
            error(err)
            return False

    def fetch_and_save_timestamp(self, **kwargs):
        """
        fetch and save timestamp
        :return: {unix time/ datetime}
        """
        new_timestamp = kwargs.get('new_timestamp', None)

        try:
            last_run_time = self.fetch_timestamp()
            self.save_timestamp(new_timestamp=new_timestamp)
            return last_run_time
        except Exception as err:
            error(err)
            return False

    def fetch_timestamp(self, **kwargs):
        """
        get timestamp
        :param datetime_format: {boolean} if datetime - return timestamp as datetime
        :return: {unix time/ datetime}
        """
        save_file_path = os.path.join(self.run_folder, self.TIMESTAMP)
        last_run_time = 0
        if os.path.isfile(save_file_path):
            with open(save_file_path, 'r') as f:
                last_run_time = f.read()
                f.close()
        last_run_time = int(last_run_time)
        if kwargs.get('datetime_format'):
            if len(str(last_run_time)) == 13:
                last_run_time = last_run_time / 1000
            last_run_time = datetime.fromtimestamp(last_run_time)
        return last_run_time
