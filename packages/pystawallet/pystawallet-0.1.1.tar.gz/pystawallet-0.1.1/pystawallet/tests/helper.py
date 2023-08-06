import socket
import unittest

from nanohttp import quickstart

from pystawallet import StawalletApiClient
from pystawallet.tests.mock_api_server import StawalletRootMockController, valid_mock_api_key, \
    valid_mock_api_secret


class ApiClientTestCase(unittest.TestCase):
    _server_shutdown = None
    api_client = None

    @classmethod
    def find_free_port(cls):
        s = socket.socket()
        s.bind(('', 0))  # Bind to a free port provided by the host.
        port = s.getsockname()[1]  # Return the port number assigned.
        s.close()
        return port

    @classmethod
    def setUpClass(cls):
        server_port = cls.find_free_port()
        cls._server_shutdown = quickstart(
            controller=StawalletRootMockController(),
            port=server_port,
            block=False
        )
        cls.api_client = StawalletApiClient(
            api_key=valid_mock_api_key,
            api_secret=valid_mock_api_secret,
            base_url=f'http://localhost:{server_port}'
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls._server_shutdown()
        super().tearDownClass()
