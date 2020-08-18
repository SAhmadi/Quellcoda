import os
import unittest
from typing import Tuple, List

from flask import Flask, request
from werkzeug.datastructures import FileStorage, MultiDict
from blueprints.serverless_testing import views
from blueprints.serverless_testing.exec_types.exec_types import ExecType
from tests.serverless_testing.utils import GRADLE_PROJECT_PATH, GRADLE_PROJECT_FILENAME, CONTENT_TYPE_ZIP, \
    CONTENT_TYPE_FORM_DATA, CONTENT_TYPE_JSON, GRADLE_WITH_ARGS_PATH, GRADLE_WITH_ARGS_FILENAME


def init_req_objs_gradle() -> Tuple[MultiDict, List[FileStorage]]:
    """Initializes the flask request object for the
    endpoints /run/gradle and /test/gradle

    :return: The data and files send with the request.
    :rtype: Tuple[MultiDict, List[FileStorage]]
    """
    gradle_file = FileStorage(stream=open(GRADLE_PROJECT_PATH, 'rb'),
                              filename=GRADLE_PROJECT_FILENAME,
                              content_type=CONTENT_TYPE_ZIP)

    data = MultiDict([
        ('file', gradle_file)
    ])

    return data, [gradle_file]


def init_req_objs_gradle_with_args() -> Tuple[MultiDict, List[FileStorage]]:
    """Initializes the flask request object for the
    endpoints /run/gradle?args1=Args Endpoint

    :return: The data and files send with the request.
    :rtype: Tuple[MultiDict, List[FileStorage]]
    """
    gradle_file = FileStorage(stream=open(GRADLE_WITH_ARGS_PATH, 'rb'),
                              filename=GRADLE_WITH_ARGS_FILENAME,
                              content_type=CONTENT_TYPE_ZIP)

    data = MultiDict([
        ('file', gradle_file)
    ])

    return data, [gradle_file]


class TestGradleViews(unittest.TestCase):
    """Tests gradle routes.
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

    def test_endpoint_run_gradle(self):
        """Tests endpoint /run/gradle.
        """
        self.data, self.files = init_req_objs_gradle()
        with self.app.test_request_context('/run/gradle',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_gradle(request, exec_type=ExecType.run)

        self.assertEqual(resp.status_code, 200)

    def test_endpoint_run_gradle_return_json(self):
        """Tests endpoint /run/gradle?return=json.
        """
        self.data, self.files = init_req_objs_gradle()
        with self.app.test_request_context('/run/gradle?return=json',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_gradle(request, exec_type=ExecType.run)

        self.assertEqual(resp[0].content_type, CONTENT_TYPE_JSON)

    def test_endpoint_run_gradle_with_args(self):
        """Tests endpoint /run/gradle?args1=0&args2=100&args3=2.
        """
        self.data, self.files = init_req_objs_gradle_with_args()
        with self.app.test_request_context('/run/gradle?args1=0&args2=100&args3=2',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_gradle(request, exec_type=ExecType.run)

        self.assertEqual(resp.status_code, 200)

    def test_endpoint_test_gradle(self):
        """Tests endpoint /test/gradle.
        """
        self.data, self.files = init_req_objs_gradle()
        with self.app.test_request_context('/test/gradle',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_gradle(request, exec_type=ExecType.test)

        self.assertEqual(resp.status_code, 200)

    def test_endpoint_test_gradle_return_json(self):
        """Tests endpoint /test/gradle?return=json.
        """
        self.data, self.files = init_req_objs_gradle()
        with self.app.test_request_context('/test/gradle?return=json',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_gradle(request, exec_type=ExecType.test)

        self.assertEqual(resp[0].content_type, CONTENT_TYPE_JSON)
