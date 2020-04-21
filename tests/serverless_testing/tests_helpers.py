import unittest
from flask import Flask
from werkzeug.datastructures import MultiDict
from blueprints.serverless_testing.helpers import check_files


class TestHelpers(unittest.TestCase):
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

    def tearDown(self):
        """Cleanup "app_context".
        """
        self.app_context.pop()

    def test_check_files_if_not_present(self):
        """Tests :meth:check_files if no "file" form parameter in request.
        """
        __request_files = MultiDict([
            ('no_file', 'MockFile.java'),
            ('no_file', 'FooFile.java'),
            ('main_file', 'MyMainClass')
        ])
        files, err = check_files(__request_files, allowed_extensions=['java'])
        self.assertIsInstance(err, str)
