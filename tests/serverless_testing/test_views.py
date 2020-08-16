import os
import unittest
from typing import Tuple, List

from flask import Flask, request
from werkzeug.datastructures import FileStorage, MultiDict
from blueprints.serverless_testing import views
from blueprints.serverless_testing.exec_types.exec_types import ExecType
from blueprints.serverless_testing.helpers import JUNIT_PATH
from blueprints.serverless_testing.views import java

# Globals
ROOT_TEST_DIR = '/app/tests/serverless_testing/'

CONTENT_TYPE_PLAIN = 'text/plain'
CONTENT_TYPE_FORM_DATA = 'multipart/form-data'
CONTENT_TYPE_ZIP = 'application/zip'

# Filenames and paths for testing
MAIN_FILENAME = 'MyMainClass.java'
MAIN_PATH = os.path.join(ROOT_TEST_DIR, 'multiple_java_files', MAIN_FILENAME)

CALC_FILENAME = 'Calculator.java'
CALC_PATH = os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_FILENAME)

CALC_TEST_FILENAME = 'CalculatorTest.java'
CALC_TEST_PATH = os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_TEST_FILENAME)

GRADLE_PROJECT_FILENAME = 'gradle_project.zip'
GRADLE_PROJECT_PATH = os.path.join(ROOT_TEST_DIR, 'gradle_project', GRADLE_PROJECT_FILENAME)


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


def init_req_objs_run_gradle() -> Tuple[MultiDict, List[FileStorage]]:
    """Initializes the flask request object for the endpoint /run/gradle

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


class TestViews(unittest.TestCase):
    """Tests compile and execute functions inside views.
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
        self.app_context.pop()
        for f in self.files:
            f.close()

    def test_endpoint_run_java(self):
        """Tests endpoint /run/java.
        """
        self.data, self.files = init_req_objs_run_java()
        with self.app.test_request_context('/run/java',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_java(request, exec_type=ExecType.run)

        [f.close() for f in self.files]
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

        [f.close() for f in self.files]
        self.assertEqual(resp.status_code, 200)

    def test_endpoint_run_gradle(self):
        """Tests endpoint /run/gradle.
        """
        self.data, self.files = init_req_objs_run_gradle()
        with self.app.test_request_context('/run/gradle',
                                           data=self.data,
                                           method='POST',
                                           content_type=CONTENT_TYPE_FORM_DATA):
            resp = views.execute_zip(request, exec_type=ExecType.run, use_gradle=True)

        [f.close() for f in self.files]
        self.assertEqual(resp.status_code, 200)


    # def test_compile_java_run(self):
    #     """Tests :meth:compile_java in views with
    #     execution_type set to "run".
    #     """
    #     # data = init_request_obj_java()
    #     with self.app.test_request_context('/run/java',
    #                                        data=self.data,
    #                                        method='POST',
    #                                        content_type='multipart/form-data'):
    #         __files = request.files.getlist('file')
    #         __work_path = '/app/tests/serverless_testing/multiple_java_files'
    #         __out_path = os.path.join(__work_path, 'out')
    #         __class_path = __out_path + ':' + JUNIT_PATH
    #         stdout = views.javac(execution_type='run',
    #                              files=__files,
    #                              work_path=__work_path,
    #                              out_path=__out_path,
    #                              class_path=__class_path)
    #     self.assertIs(stdout, None)
    #
    # def test_compile_java_test(self):
    #     """Tests :meth:compile_java in views with
    #     execution_type set to "test".
    #     """
    #     # data = init_request_obj_java()
    #     with self.app.test_request_context('/test/java',
    #                                        data=self.data,
    #                                        method='POST',
    #                                        content_type='multipart/form-data'):
    #         __files = request.files.getlist('file')
    #         __work_path = '/app/tests/serverless_testing/multiple_java_files'
    #         __out_path = os.path.join(__work_path, 'out')
    #         __class_path = __out_path + ':' + JUNIT_PATH
    #         stdout = views.javac('test', __files, __work_path, __out_path, __class_path)
    #     self.assertIs(stdout, None)
    #
    # def test_execute_java_run(self):
    #     """Tests :meth:execute_java in views with
    #     execution_type set to "run".
    #     """
    #     # data = init_request_obj_java()
    #     with self.app.test_request_context('/run/java',
    #                                        data=self.data,
    #                                        method='POST',
    #                                        content_type='multipart/form-data'):
    #         __path = '/app/tests/serverless_testing/multiple_java_files/out'
    #         __main_file = 'MyMainClass'
    #         stdout, err = java('run', __path, __main_file)
    #         code = 200 if err is None else 500
    #     self.assertEqual(code, 200)


if __name__ == '__main__':
    unittest.main()
