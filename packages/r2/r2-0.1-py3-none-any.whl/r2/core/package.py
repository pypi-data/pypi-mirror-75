import json
import logging
import os
from typing import AnyStr

from r2.install import Installation


class Package:
    def __init__(self, package_name: str = 'default', overwrite: bool = False):
        self._package_name = package_name
        self._overwrite = overwrite

        self._package_path = self._create_package_directory()[1]

    def _create_package_directory(self) -> (bool, AnyStr):
        abs_package_dir = os.path.join(Installation.DOWNLOAD_DIR, self._package_name)
        if os.path.exists(abs_package_dir):
            return True, abs_package_dir
        os.makedirs(abs_package_dir)
        return os.path.exists(abs_package_dir), abs_package_dir

    def save(self, endpoint, response_body):
        path, file = self._undress_endpoint(endpoint)
        self._ensure_path_exists(os.path.join(*(self._package_path, path)))

        with open(os.path.join(*(self._package_path, path, file)), 'w') as new_json:
            try:
                if isinstance(response_body, dict):
                    new_json.write(json.dumps(response_body))
                else:
                    new_json.write(response_body)
            except Exception as err:
                print(err)
                pass

    def load(self, endpoint):
        path, file = self._undress_endpoint(endpoint)
        path_exist, path_absolute = self._ensure_path_exists(os.path.join(*(self._package_path, path)))
        if not os.path.exists(path_absolute):
            return None
        if not os.path.isfile(os.path.join(path_absolute, file)):
            return None

        with open(os.path.join(path_absolute, file), 'r') as stored_response:
            json_response = None
            raw_response = stored_response.read()
            try:
                json_response = json.loads(raw_response)
            except Exception as err:
                logging.error(f"Can not convert raw_response into json format. Is file corrupted?\n{err}")
            finally:
                return json_response

    def _ensure_path_exists(self, path: str):
        if os.path.exists(path):
            return True, path
        os.makedirs(os.path.join(self._package_path, path), exist_ok=True)
        return os.path.exists(path), path

    @staticmethod
    def _undress_endpoint(endpoint: str) -> (str, str):
        l_endpoint = endpoint.split('/')
        if len(l_endpoint) > 1:
            path, filename = os.path.relpath(os.path.join(*l_endpoint[:-1])), l_endpoint[-1]
        else:
            path, filename = '', l_endpoint[-1]
        return path, filename
