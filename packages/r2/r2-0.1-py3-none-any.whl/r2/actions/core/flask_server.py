import json
import logging
from json.decoder import JSONDecodeError
from os import makedirs
from os.path import join, exists, abspath
from typing import Union, Any

import requests
import urllib3
from flask import Flask, request, abort, jsonify, Response
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from r2.core.package import Package
from r2.configuration import Configuration
from r2.install import Installation

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FlaskServer:
    app = Flask(__name__)

    def __init__(self, target: str = None, package: str = 'default', save: bool = True, overwrite: bool = False,
                 mode: int = 1):
        if not target:
            logging.info("Working in REPLAY MODE")
        else:
            logging.info("Working in RECORD MODE")

        self.target = target
        self.package = package
        self.save = save
        self.overwrite = overwrite
        self.mode = mode

        self._download_dir = abspath(Installation.DOWNLOAD_DIR)
        self.abs_package_path = join(self._download_dir, package)
        if not exists(self.abs_package_path):
            makedirs(self.abs_package_path, exist_ok=True)

    def __call__(self):
        self.app.run()

    def serve(self):
        self.__call__()

    @staticmethod
    def dump_content(endpoint, response_body):
        package = Package(Configuration.read()["package_name"], True)
        package.save(endpoint, response_body)

    @staticmethod
    def load_content(endpoint):
        package = Package(Configuration.read()["package_name"])
        if not package.load(endpoint):
            return Response(status=404)
        else:
            return package

    @staticmethod
    @app.route('/favicon.ico')
    def favicon():
        return abort(404, description="Resource not found")

    @staticmethod
    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PATCH", "DELETE"], strict_slashes=False)
    @app.route('/<path:path>', methods=["GET", "POST", "PATCH", "DELETE"], strict_slashes=False)
    def catch_traffic(path):
        headers = request.headers
        request_data = request.get_data().decode("utf-8")
        payload = None
        if request.content_type and request.content_type.lower() == 'application/json':
            try:
                payload = json.loads(request_data)
            except json.JSONDecodeError as err:
                print(err)
                payload = {}

        return FlaskServer.release_traffic(path, "GET", payload, headers)

    @staticmethod
    def release_traffic(path, method, payload, headers) -> Union[bytes, Any]:
        target = Configuration().read()["target"]
        mode = Configuration().read()["mode"]

        endpoint = f'{target}/{path}'
        if request.query_string:
            endpoint = f'{endpoint}?{request.query_string.decode("utf-8")}'

        # record mode == 0
        if mode == 0:
            return FlaskServer._record_mode(payload, method, endpoint, path, headers)
        elif mode == 1:
            return FlaskServer._replay_mode(path)
        else:
            raise NotImplementedError

    @staticmethod
    def _replay_mode(path):
        stored_target_response = FlaskServer.load_content(path)
        logging.info(f"Found stored response for path {path}")
        return stored_target_response

    @staticmethod
    def _record_mode(payload, method, endpoint, path, headers):
        # kwargs = {'verify': False,
        #           'headers': headers}
        kwargs = {'verify': False}
        if payload:
            if headers['Content-Type'] == "application/json":
                kwargs['data'] = json.dumps(payload)
            else:
                kwargs['data'] = payload

        request_method = {'GET': requests.get,
                          'POST': requests.post,
                          'PATCH': requests.patch,
                          'DELETE': requests.delete}[method.upper()]
        response = request_method(endpoint, **kwargs)

        status_code, response_body, headers = response.status_code, response.content.decode("utf-8"), response.headers
        logging.info(endpoint)
        try:
            target_response = json.loads(response_body)
            FlaskServer.dump_content(path, target_response)

            logging.info(f"Received a response from the target for the path {path}")
            return target_response
        except JSONDecodeError:
            logging.error("JSON response is corrupted")
            return jsonify({"r2error": "JSON response is corrupted"})


if __name__ == "__main__":
    f = FlaskServer(target="http://api.plos.org/", package='default')
    f()
