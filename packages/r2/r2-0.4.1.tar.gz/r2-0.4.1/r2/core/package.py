import json
import logging
import os
from typing import AnyStr, Dict

from r2.install import Installation


class Package:
    def __init__(self, package_name: str = 'default', overwrite: bool = False):
        self._package_name = package_name
        self._overwrite = overwrite

        self._package_path = self._create_package_directory()[1]

    def _create_package_directory(self) -> (bool, AnyStr):
        abs_package_dir = os.path.join(Installation.PACKAGES_DIR, self._package_name)
        if os.path.exists(abs_package_dir):
            return True, abs_package_dir
        os.makedirs(abs_package_dir)
        return os.path.exists(abs_package_dir), abs_package_dir

    def save(self, endpoint, response_body) -> bool:
        path, file, args = self._undress_endpoint(endpoint)
        self._ensure_path_exists(os.path.join(*(self._package_path, path)))
        response_path = os.path.join(*(self._package_path, path, file))

        outer_template = {
            "data_id": os.path.join(path, file),
            "actions": []
        }

        inner_template = {
            "arguments": {},
            "response": None
        }

        template = outer_template
        if os.path.isfile(response_path):
            existing_file = self._load_existing_file(response_path)
            template = existing_file if existing_file.get("data_id", False) else outer_template

        # noinspection PyTypeChecker
        known_arguments = [x for x in template["actions"] if args != x["arguments"]]

        inner_template["arguments"], inner_template["response"] = args, response_body
        known_arguments.append(inner_template)

        template["actions"] = known_arguments

        with open(response_path, 'w') as new_json:
            try:
                if isinstance(template, dict):
                    new_json.write(json.dumps(template))
                else:
                    new_json.write(str(template))
            except Exception as err:
                print(err)
                return False
            return True

    def _load_existing_file(self, path):
        existing_file = json.loads(self.__read(path))
        if not isinstance(existing_file, dict):
            return
        return existing_file

    def load(self, endpoint):
        _, _, args = self._undress_endpoint(endpoint)
        proper_response_base_on_args = [x for x in self.get_all_actions(endpoint) if args == x["arguments"]]

        load_response = proper_response_base_on_args[0]["response"] if proper_response_base_on_args else None

        try:
            if isinstance(load_response, dict):
                return load_response

            if load_response is not None:
                load_response = json.loads(load_response)
            else:
                raise
        except TypeError as e:
            load_response = {
                "r2_error": f'{e}',
                "r2_raw_content": load_response
            }
        return load_response

    def get_all_actions(self, endpoint):
        path, file, _ = self._undress_endpoint(endpoint)
        path_exist, path_absolute = self._ensure_path_exists(os.path.join(*(self._package_path, path)))
        if not os.path.exists(path_absolute):
            return None
        if not os.path.isfile(os.path.join(path_absolute, file)):
            return None

        json_response = None
        raw_response = self.__read(os.path.join(path_absolute, file))
        try:
            json_response = json.loads(raw_response)
        except Exception as err:
            logging.error(f"Can not convert raw_response into json format. Is file corrupted?\n{err}")
        return json_response["actions"]

    @staticmethod
    def __read(location):
        with open(location, 'r') as stored_response:
            return stored_response.read()

    @staticmethod
    def __save(location, content):
        with open(location, 'w') as file_store:
            file_store.write(content)

    def _ensure_path_exists(self, path: str):
        if os.path.exists(path):
            return True, path
        os.makedirs(os.path.join(self._package_path, path), exist_ok=True)
        return os.path.exists(path), path

    def _undress_endpoint(self, endpoint: str) -> (AnyStr, AnyStr, Dict):
        l_endpoint = endpoint.split('/')
        if len(l_endpoint) > 1:
            path, filename = os.path.relpath(os.path.join(*l_endpoint[:-1])), l_endpoint[-1]
        else:
            path, filename = '', l_endpoint[-1]
        args = self._make_args_dict_from_endpoint(endpoint)
        if args:
            filename = filename.split('?')[0]
        return path, filename, args

    @staticmethod
    def _make_args_dict_from_endpoint(endpoint) -> Dict:
        if '?' not in endpoint:
            return {}
        arguments = endpoint.split('?')[1:][0].split('&')
        args: Dict = {}
        for next_pair in arguments:
            k, v = next_pair.split('=')
            args[k] = v
        return args
