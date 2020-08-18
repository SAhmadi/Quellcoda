import os
import shutil
import unittest
from flask import Flask

from blueprints.serverless_testing.exec_types.compile import javac
from blueprints.serverless_testing.exec_types.exec_types import ExecType
from blueprints.serverless_testing.exec_types.execute import java
from blueprints.serverless_testing.helpers import JUNIT_PATH
from tests.serverless_testing.utils import ROOT_TEST_DIR, CALC_FILENAME, CALC_TEST_FILENAME, MAIN_FILENAME, \
    HELLO_NAME_FILENAME


class TestCommandJava(unittest.TestCase):
    """Tests if java command can execute compiled Java files.
    """
    def setUp(self):
        """Setup "app_context" and "client", so we can get
        flask request object.
        """
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Compile and run or test files
        self.out_path = os.path.join(ROOT_TEST_DIR, 'multiple_java_files', 'out')
        self.class_path = self.out_path + ':' + JUNIT_PATH

    def tearDown(self):
        """Cleanup "app_context".
        """
        # Remove out/ dir containing already compiled files
        shutil.rmtree(self.out_path, ignore_errors=True)
        self.app_context.pop()

    def test_java_command_success_for_run(self):
        """Tests the success of java command with exec_type "run".
        """
        file_paths = [
            os.path.join(ROOT_TEST_DIR, 'multiple_java_files', MAIN_FILENAME),
            os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_FILENAME)
        ]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=self.out_path,
                               class_path=self.class_path)

        if stdout is None and stderr is None:
            # Execute compiled java files
            result, err = java(exec_type=ExecType.run,
                               class_path=self.class_path,
                               main_file=MAIN_FILENAME.rsplit('.', maxsplit=1)[0],
                               args=[])

            self.assertIsNone(err)

    def test_java_command_failure_for_run(self):
        """Tests the failure of java command with exec_type "run".
        """
        file_paths = [os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_TEST_FILENAME)]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=self.out_path,
                               class_path=self.class_path)

        if stdout is None and stderr is None:
            # Execute compiled java files
            result, err = java(exec_type=ExecType.run,
                               class_path=self.class_path,
                               main_file=CALC_TEST_FILENAME.rsplit('.', maxsplit=1)[0],
                               args=[])

            self.assertIsNotNone(err)

    def test_java_command_success_for_run_with_args(self):
        """Tests the success of java command with exec_type "run" and
        sends args.
        """
        file_paths = [
            os.path.join(ROOT_TEST_DIR, 'arguments', HELLO_NAME_FILENAME)
        ]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=self.out_path,
                               class_path=self.class_path)

        if stdout is None and stderr is None:
            # Execute compiled java files
            result, err = java(exec_type=ExecType.run,
                               class_path=self.class_path,
                               main_file=HELLO_NAME_FILENAME.rsplit('.', maxsplit=1)[0],
                               args=["Alice"])

            self.assertIsNone(err)

    def test_java_command_success_for_test(self):
        """Tests the success of java command with exec_type "test".
        """
        file_paths = [
            os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_FILENAME),
            os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_TEST_FILENAME)
        ]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=self.out_path,
                               class_path=self.class_path)

        if stdout is None and stderr is None:
            # Execute compiled java files
            result, err = java(exec_type=ExecType.run,
                               class_path=self.class_path,
                               main_file=None,
                               args=[])

            self.assertIsNotNone(result)

    def test_java_command_failure_for_test(self):
        """Tests the failure of java command with exec_type "test".
        """
        file_paths = [os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_TEST_FILENAME)]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=self.out_path,
                               class_path=self.class_path)

        if stdout is None and stderr is None:
            # Execute compiled java files
            result, err = java(exec_type=ExecType.run,
                               class_path=self.class_path,
                               main_file=None,
                               args=[])

            self.assertIsNotNone(err)
