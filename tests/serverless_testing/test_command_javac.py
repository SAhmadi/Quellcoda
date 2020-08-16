import os
import shutil
import unittest
from flask import Flask

from blueprints.serverless_testing.exec_types.compile import javac
from blueprints.serverless_testing.helpers import JUNIT_PATH
from tests.serverless_testing.utils import ROOT_TEST_DIR, CALC_FILENAME, CALC_TEST_FILENAME, MAIN_FILENAME


class TestCommandJavac(unittest.TestCase):
    """Tests if javac command can compile Java source code
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

    def test_javac_command_success(self):
        """Tests the success of javac command.
        """
        file_paths = [
            os.path.join(ROOT_TEST_DIR, 'multiple_java_files', MAIN_FILENAME),
            os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_FILENAME)
        ]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=self.out_path,
                               class_path=self.out_path)

        self.assertIsNone(stdout)
        self.assertIsNone(stderr)

    def test_javac_command_failure(self):
        """Tests the failure of javac command.
        """
        file_paths = [os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_TEST_FILENAME)]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=self.out_path,
                               class_path=self.class_path)

        self.assertIsNotNone(stderr)
