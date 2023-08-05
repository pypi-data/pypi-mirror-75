import logging
from os import makedirs
from os.path import expanduser, join, exists


class Installation:
    HOME_DIR: str = join(expanduser('~'), '.r2')
    DOWNLOAD_DIR: str = join(HOME_DIR, "download")

    def __init__(self):
        self._create_default_directories()
        self._verifies_directories()

    def _create_default_directories(self):
        for d in (self.HOME_DIR, self.DOWNLOAD_DIR):
            makedirs(d, exist_ok=True)

    def _verifies_directories(self):
        for d in (self.HOME_DIR, self.DOWNLOAD_DIR):
            if not exists(d):
                logging.error(f"Can not create a {d} directory")
                raise

    @property
    def download_path(self):
        return self.DOWNLOAD_DIR
