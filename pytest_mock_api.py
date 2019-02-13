# -*- coding: utf-8 -*-

import pytest
import requests

from flask import jsonify
from threading import Thread


def pytest_addoption(parser):
    group = parser.getgroup('mock-api')
    group.addoption(
        '--port',
        action='store',
        dest='dest_port',
        default=5000,
        help='Set the port for the server. default=5000'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.fixture
def mock_api(request):
    return request.config.option.dest_foo


class MockApi(Thread):
    def __init__(self, port=5000):
        super().__init__()
        from flask import Flask
        self.port = port
        self.app = Flask(__name__)
        self.url = f"http://localhost:{str(self.port)}"

        self.app.add_url_rule("/shutdown", view_func=self._shutdown_server)
        self.app.add_url_rule("/<string:path>", view_func=self._reroute_to_api)

    def _reroute_to_api(self):
        pass

    def _shutdown_server(self):
        from flask import request
        if 'werkzeug.server.shutdown' not in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):
        requests.get(f"http://localhost:{str(self.port)}/shutdown")
        self.join()

    def add_callback_response(self, url, endpoint, callback, methods=("GET",)):
        self.app.add_url_rule(
            url, endpoint=endpoint, view_func=callback, methods=methods
        )

    def add_json_response(self, url, endpoint, serializable, methods=("GET",)):
        def callback():
            return jsonify(serializable)

        self.add_callback_response(url, endpoint, callback, methods=methods)

    def run(self):
        self.app.run(port=self.port)
