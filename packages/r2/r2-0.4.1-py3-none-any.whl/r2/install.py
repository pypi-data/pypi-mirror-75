import logging
from os import makedirs
from os.path import expanduser, join, exists, abspath


class Installation:
    HOME_DIR: str = join(expanduser('~'), '.r2')
    PACKAGES_DIR: str = join(HOME_DIR, "packages")
    LOGS_DIR: str = join(HOME_DIR, "logs")

    def __init__(self):
        self._create_default_directories()
        self._verifies_directories()

    def _create_default_directories(self):
        for d in (self.HOME_DIR, self.PACKAGES_DIR, self.LOGS_DIR):
            makedirs(d, exist_ok=True)

    def _verifies_directories(self):
        for d in (self.HOME_DIR, self.PACKAGES_DIR, self.LOGS_DIR):
            if not exists(d):
                logging.error(f"Can not create a {d} directory")
                raise

    @staticmethod
    def package_directory_creation(package):
        _packages_dir = abspath(Installation.PACKAGES_DIR)
        abs_package_path = join(_packages_dir, package)
        if not exists(abs_package_path):
            makedirs(abs_package_path, exist_ok=True)
