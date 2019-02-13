# -*- coding: utf-8 -*-

import pytest
from mock_api import MockApi


def pytest_addoption(parser):
    group = parser.getgroup('mock-api')
    group.addoption(
        '--port',
        action='store',
        dest='dest_port',
        default=5000,
        help='Set the port for the server. default=5000'
    )

    parser.addini('mock_api_port', 'Set the port for the server. default=5000')


@pytest.fixture(scope="function", autouse=True)
def mock_api(request):
    target_port = request.config.option.dest_port
    this_mock_api = MockApi(port=int(target_port))
    this_mock_api.start()
    yield this_mock_api
    this_mock_api.shutdown_server()
