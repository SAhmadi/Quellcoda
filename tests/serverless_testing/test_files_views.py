import unittest
from typing import Tuple, List

from flask import Flask, request
from werkzeug.datastructures import FileStorage, MultiDict
from blueprints.serverless_testing import views
from blueprints.serverless_testing.exec_types.exec_types import ExecType
from tests.serverless_testing.utils import MAIN_PATH, MAIN_FILENAME, CALC_PATH, CALC_FILENAME, CALC_TEST_PATH, \
    CALC_TEST_FILENAME, CONTENT_TYPE_FORM_DATA, CONTENT_TYPE_PLAIN, CONTENT_TYPE_JSON, HELLO_NAME_PATH, \
    HELLO_NAME_FILENAME


def init_req_objs_run_java() -> Tuple[MultiDict, List[FileStorage]]:
    """Initializes the flask request object for the endpoint /run/java

    :return: The data and files send with the request.
    :rtype: Tuple[MultiDict, List[FileStorage]]
    """
    main_file = FileStorage(stream=open(MAIN_PATH, 'rb'),
                            filename=MAIN_FILENAME,
                            content_type=CONTENT_TYPE_PLAIN)

    calculator_file = FileStorage(stream=open(CALC_PATH, 'rb'),
                                  filename=CALC_FILENAME,
                                  content_type=CONTENT_TYPE_PLAIN)

    data = MultiDict([
        ('main_file', MAIN_FILENAME),
        ('file', main_file),
        ('file', calculator_file),
    ])

    return data, [main_file, calculator_file]


def init_req_objs_run_java_with_args() -> Tuple[MultiDict, List[FileStorage]]:
    """Initializes the flask request object for the endpoint /run/java?args1=Value

    :return: The data and files send with the request.
    :rtype: Tuple[MultiDict, List[FileStorage]]
    """
    hello_name = FileStorage(stream=open(HELLO_NAME_PATH, 'rb'),
                             filename=HELLO_NAME_FILENAME,
                             content_type=CONTENT_TYPE_PLAIN)

    data = MultiDict([
        ('main_file', HELLO_NAME_FILENAME),
        ('file', hello_name),
    ])

    return data, [hello_name]


def init_req_objs_test_java() -> Tuple[MultiDict, List[FileStorage]]:
    """Initializes the flask request object for the endpoint /test/java

    :return: The data and files send with the request.
    :rtype: Tuple[MultiDict, List[FileStorage]]
    """
    calculator_file = FileStorage(stream=open(CALC_PATH, 'rb'),
                                  filename=CALC_FILENAME,
                                  content_type=CONTENT_TYPE_PLAIN)

    calculator_test_file = FileStorage(stream=open(CALC_TEST_PATH, 'rb'),
                                       filename=CALC_TEST_FILENAME,
                                       content_type=CONTENT_TYPE_PLAIN)

    data = MultiDict([
        ('file', calculator_file),
        ('file', calculator_test_file),
    ])

    return data, [calculator_file, calculator_test_file]


class TestFileViews(unittest.TestCase):
    """Tests Java file routes.
    """

    def setUp(self):
        """Setup "app_context" and "client", so we can get
        flask request object.
        """
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Cleanup "app_context".
        """
        for f in self.files:
            f.close()
        self.app_context.pop()

    def test_endpoint_run_java(self):
        """Tests endpoint /run/java.
        """
        self.data, self.files = init_req_objs_run_java()
        with self.app.test_request_context('/run/java',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_java(request, exec_type=ExecType.run)

        self.assertEqual(resp.status_code, 200)

    def test_endpoint_run_java_with_args(self):
        """Tests endpoint /run/java?args1=Alice.
        """
        self.data, self.files = init_req_objs_run_java_with_args()
        with self.app.test_request_context('/run/java?args1=Alice',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_java(request, exec_type=ExecType.run)

        self.assertEqual(resp.status_code, 200)

    def test_endpoint_tests_java(self):
        """Tests endpoint /test/java.
        """
        self.data, self.files = init_req_objs_test_java()
        with self.app.test_request_context('/test/java',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_java(request, exec_type=ExecType.test)

        self.assertEqual(resp.status_code, 200)
