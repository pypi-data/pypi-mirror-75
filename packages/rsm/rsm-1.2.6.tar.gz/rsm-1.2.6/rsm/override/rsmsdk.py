from rsm.handlers.logging import LogHandler
from typing import NoReturn
import json
import os

log = LogHandler()
debug = log.logger.debug
info = log.logger.info
error = log.logger.error


class EnvironmentVarNames(object):
    APP_IP = "APP_IP"


class RsmSDK:
    debug('The `RsmSDK` class is used to replace `SiemplifySdkConfig`')

    def __init__(self) -> NoReturn:
        current_module_path = os.path.dirname(os.path.abspath(__file__))
        sdk_config_path = os.path.join(current_module_path, "sdk_config.json")

        self.api_root_uri = "https://localhost:8443/api"
        self.config_files_root_path = "/opt/siemplify/siemplify_server/Configs"
        self.run_folder_path = "/opt/siemplify/siemplify_server/bin/Scripting"
        self.is_remote_publisher_sdk = False

        if os.path.isfile(sdk_config_path):
            try:
                with open(sdk_config_path, "r") as configFile:
                    config = json.loads(configFile.read())

                    # Added this line below to prevent from getting a Windows path
                    # since Siemplify does not update their `sdk_config.json` file.

                    if not config.get('config_files_root_path').startswith("C:"):
                        debug('The `sdk_config` file does not start with C:, it should be up to date')
                        self.config_files_root_path = config.get("config_files_root_path")
                        self.run_folder_path = config.get("run_folder_path")

                    # Determines whether or not the connector/action is running from a Remote Agent.
                    self.is_remote_publisher_sdk = config.get("is_remote_publisher_sdk", False)
            except Exception as e:
                error("Failed to load the configuration file: " + str(e))

        self.override_with_environment_vars()

    def override_with_environment_vars(self) -> NoReturn:
        # load params from environment variables, override (give highest priority)
        simplify_app_ip_from_environment = os.environ.get(EnvironmentVarNames.APP_IP)

        if simplify_app_ip_from_environment:
            self.api_root_uri = "https://" + simplify_app_ip_from_environment + ":8443/api"