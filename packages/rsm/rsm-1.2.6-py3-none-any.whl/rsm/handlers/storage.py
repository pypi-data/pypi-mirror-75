from typing import NoReturn
from pathlib import Path
import getpass
import os


class CustomDataStore:
    def __call__(self, integration, script_name) -> NoReturn:
        self.integration = integration
        self.script_name = script_name

        # Not using Path.home() to prevent getting fooled by environment variable.

        self.basedir = Path(
            os.path.expanduser(
                '~{0}'.format(
                    getpass.getuser()))) / 'custom'

        return self.__init_custom_basedir(), self.__init_integration_folder()

    def __init_integration_folder(self) -> NoReturn or Exception:
        n = [self.integration, self.script_name]
        try:
            for idx, path in enumerate(n):
                previous = "/".join(n[:idx]) if idx > 0 else ''
                self.__is_dir(self.basedir / previous / path)
        except Exception as err:
            return err
        return self.__is_dir(
            self.basedir /
            self.integration /
            self.script_name)

    def __init_custom_basedir(self) -> NoReturn:
        return self.__is_dir(self.basedir)

    @property
    def ds_path(self) -> Path:
        return self.basedir / self.integration / self.script_name

    @staticmethod
    def __is_dir(dirpath: Path) -> NoReturn:
        dirpath.mkdir(mode=0o775, exist_ok=True)
