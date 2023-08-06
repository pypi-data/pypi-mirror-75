import json
from dataclasses import dataclass
from os.path import join
from typing import Dict

from r2.install import Installation


@dataclass
class Configuration:
    TARGET: str = None
    PACKAGE_NAME: str = None
    MODE: int = None

    def _config_dict(self):
        return {
            "target": self.TARGET,
            "package_name": self.PACKAGE_NAME,
            "mode": self.MODE
        }

    @staticmethod
    def read():
        with open(Configuration.__config_path(), 'r') as config_file:
            return json.loads(config_file.read())

    @staticmethod
    def write(config_dict: Dict):
        with open(Configuration.__config_path(), 'w') as config_file:
            config_file.write(json.dumps(config_dict))

    def save(self):
        self.write(self._config_dict())

    @staticmethod
    def __config_path():
        return join(Installation.HOME_DIR, "config.r2")
