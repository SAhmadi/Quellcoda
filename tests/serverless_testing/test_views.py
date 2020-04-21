import os
import unittest
from typing import Tuple, List

from flask import Flask, request
from werkzeug.datastructures import FileStorage, MultiDict
from blueprints.serverless_testing import views
from blueprints.serverless_testing.helpers import JUNIT_PATH
from blueprints.serverless_testing.views import execute_java


def init_request_obj_java() -> Tuple[MultiDict, List[FileStorage]]:
    """Initializes the flask request object.
    :return: The data and files send with the request.
    :rtype: Tuple[MultiDict, List[FileStorage]]
    """
    root_dir = '/app/tests/serverless_testing/multiple_java_files'
    # out_path = '{0}/out'.format(root_dir)

    main_file_path = os.path.join('{0}/MyMainClass.java'.format(root_dir))
    calculator_file_path = os.path.join('{0}/Calculator.java'.format(root_dir))
    calculator_test_file_path = os.path.join('{0}/CalculatorTest.java'.format(root_dir))

    main_file = FileStorage(stream=open(main_file_path, 'rb'),
                            filename='MyMainClass.java',
                            content_type='text/plain')
    calculator_file = FileStorage(stream=open(calculator_file_path, 'rb'),
                                  filename='Calculator.java',
                                  content_type='text/plain')
    calculator_test_file = FileStorage(stream=open(calculator_file_path, 'rb'),
                                       filename='CalculatorTest.java',
                                       content_type='text/plain')

    # main_file.close()
    # calculator_file.close()

    data = MultiDict([
        ('file', main_file),
        ('file', calculator_file),
        ('file', calculator_test_file),
        ('main_file', 'MyMainClass')
    ])

    return data, [main_file, calculator_file, calculator_test_file]


class TestViews(unittest.TestCase):
    """Tests compile and execution functions inside views.
    """
    def setUp(self):
        """Setup "app_context" and "client", so we can get
        flask request object.
        """
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.data, self.files = init_request_obj_java()

    def tearDown(self):
        """Cleanup "app_context".
        """
        self.app_context.pop()
        for f in self.files:
            f.close()

    def test_compile_and_execute_java_run(self):
        """Tests :meth:compile_and_execute_java in views
        with execution_type set to "run".
        """
        # data = init_request_obj_java()
        with self.app.test_request_context('/run/java',
                                           data=self.data,
                                           method='POST',
                                           content_type='multipart/form-data'):
            resp, _ = views.compile_and_execute_java(request, execution_type='run')
        self.assertEqual(resp.status_code, 200)

    def test_compile_and_execute_java_test(self):
        """Tests :meth:compile_and_execute_java in views
        with execution_type set to "test".
        """
        # data = init_request_obj_java()
        with self.app.test_request_context('/test/java',
                                           data=self.data,
                                           method='POST',
                                           content_type='multipart/form-data'):
            resp, _ = views.compile_and_execute_java(request, execution_type='test')
        self.assertEqual(resp.status_code, 200)

    def test_compile_java_run(self):
        """Tests :meth:compile_java in views with
        execution_type set to "run".
        """
        # data = init_request_obj_java()
        with self.app.test_request_context('/run/java',
                                           data=self.data,
                                           method='POST',
                                           content_type='multipart/form-data'):
            __files = request.files.getlist('file')
            __work_path = '/app/tests/serverless_testing/multiple_java_files'
            __out_path = os.path.join(__work_path, 'out')
            __class_path = __out_path + ':' + JUNIT_PATH
            stdout = views.compile_java(execution_type='run',
                                        files=__files,
                                        work_path=__work_path,
                                        out_path=__out_path,
                                        class_path=__class_path)
        self.assertIs(stdout, None)

    def test_compile_java_test(self):
        """Tests :meth:compile_java in views with
        execution_type set to "test".
        """
        # data = init_request_obj_java()
        with self.app.test_request_context('/test/java',
                                           data=self.data,
                                           method='POST',
                                           content_type='multipart/form-data'):
            __files = request.files.getlist('file')
            __work_path = '/app/tests/serverless_testing/multiple_java_files'
            __out_path = os.path.join(__work_path, 'out')
            __class_path = __out_path + ':' + JUNIT_PATH
            stdout = views.compile_java('test', __files, __work_path, __out_path, __class_path)
        self.assertIs(stdout, None)

    def test_execute_java_run(self):
        """Tests :meth:execute_java in views with
        execution_type set to "run".
        """
        # data = init_request_obj_java()
        with self.app.test_request_context('/run/java',
                                           data=self.data,
                                           method='POST',
                                           content_type='multipart/form-data'):
            __path = '/app/tests/serverless_testing/multiple_java_files/out'
            __main_file = 'MyMainClass'
            stdout, err = execute_java('run', __path, __main_file)
            code = 200 if err is None else 500
        self.assertEqual(code, 200)


if __name__ == '__main__':
    unittest.main()
