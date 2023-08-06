import logging
from os import makedirs, mkdir
from os.path import expanduser, join, exists


class Installation:
    HOME_DIR: str = join(expanduser('~'), '.r2')
    PACKAGES_DIR: str = join(HOME_DIR, "packages")

    def __init__(self):
        self._create_default_directories()
        self._verifies_directories()

    def _create_default_directories(self):
        for d in (self.HOME_DIR, self.PACKAGES_DIR):
            makedirs(d, exist_ok=True)

    def _verifies_directories(self):
        for d in (self.HOME_DIR, self.PACKAGES_DIR):
            if not exists(d):
                logging.error(f"Can not create a {d} directory")
                raise

    @staticmethod
    def create_home():
        # noinspection PyBroadException
        try:
            mkdir(Installation.HOME_DIR)
        except Exception:
            logging.error(f"Home directory cannot be created {Installation.HOME_DIR}")

    @property
    def packages_path(self):
        return self.PACKAGES_DIR
