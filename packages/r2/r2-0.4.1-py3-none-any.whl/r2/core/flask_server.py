import json
import logging
from json.decoder import JSONDecodeError
from typing import Union, Any

import requests
import urllib3
from flask import Flask, request, abort, jsonify, Response
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from r2.configuration import Configuration
from r2.core.package import Package
from r2.helpers.server_mode import ServerMode
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

        Installation.package_directory_creation(package)

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
        package_load = package.load(endpoint)
        if not package_load:
            return Response(status=404)
        package_load = [10, 20]
        if isinstance(package_load, list):
            return Response(response=json.dumps(package_load), status=200, mimetype='application/json')
        return jsonify(package_load)

    @staticmethod
    @app.route('/favicon.ico')
    def favicon():
        return abort(404, description="Resource not found")

    @staticmethod
    @app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PATCH", "DELETE"], strict_slashes=False)
    @app.route('/<path:path>', methods=["GET", "POST", "PATCH", "DELETE"], strict_slashes=False)
    def _catch_traffic(path):
        headers = request.headers
        request_data = request.get_data().decode("utf-8")
        payload = None
        if request.content_type and request.content_type.lower() == 'application/json':
            try:
                payload = json.loads(request_data)
            except json.JSONDecodeError as err:
                print(err)
                payload = {}

        return FlaskServer._release_traffic(path, "GET", payload, headers)

    @staticmethod
    def _release_traffic(path, method, payload, headers) -> Union[bytes, Any]:
        target = Configuration().read()["target"]
        mode = ServerMode(Configuration().read()["mode"])

        endpoint = f'{target}/{path}'
        if request.query_string:
            endpoint = f'{endpoint}?{request.query_string.decode("utf-8")}'

        if mode == ServerMode.Record:
            return FlaskServer._record_mode(payload, method, endpoint, path, headers)
        elif mode == ServerMode.Replay:
            return FlaskServer._replay_mode(path)
        else:
            raise NotImplementedError

    @staticmethod
    def _replay_mode(path):
        logging.debug("Replay mode")

        stored_target_response = FlaskServer.load_content(path)
        logging.info(f"Found stored response for path {path}")

        if isinstance(stored_target_response, list):
            # noinspection PyBroadException
            try:
                return Response(response=json.dumps(stored_target_response),
                                status=200,
                                mimetype='application/json')
            except Exception:
                return Response(response=stored_target_response,
                                status=200,
                                mimetype='application/json')
        return stored_target_response

    @staticmethod
    def _record_mode(payload, method, endpoint, path, headers):
        logging.debug("Record mode")

        kwargs = {'verify': False,
                  'headers': headers}
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
        except JSONDecodeError as e:
            logging.error("JSON response is corrupted. Sending raw response")
            error_response = {
                "r2_error": f'{e}',
                "r2_raw_content": response_body
            }
            return jsonify(error_response)
        logging.info(f"Received a response from the target for the path {path}")

        if isinstance(target_response, list):
            # noinspection PyBroadException
            try:
                return Response(response=json.dumps(target_response),
                                status=200,
                                mimetype='application/json')
            except Exception:
                return Response(response=response_body,
                                status=200,
                                mimetype='application/json')

        return target_response


if __name__ == "__main__":
    f = FlaskServer(target="http://api.plos.org/", package='default')
    f()
