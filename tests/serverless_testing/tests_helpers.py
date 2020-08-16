import unittest
from flask import Flask
from werkzeug.datastructures import MultiDict
from blueprints.serverless_testing.helpers import check_files, allowed_file_exts, get_file_extension, run_cmd


class MockFileType:
    def __init__(self, filename):
        self.filename = filename


class TestHelpers(unittest.TestCase):
    """Tests helper functions.
    """
    def setUp(self):
        """Setup "app_context" and "client", so we can get
        flask request object.
        """
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.mock_file = MockFileType('MockFile.java')

    def tearDown(self):
        """Cleanup "app_context".
        """
        self.app_context.pop()

    def test_check_files_if_file_present(self):
        """Tests :meth:check_files if "file" form parameter present.
        """
        request_files = MultiDict([
            ('file', self.mock_file),
        ])
        files, err = check_files(request_files, None)
        self.assertIsNone(err)

    def test_check_files_if_no_file_present(self):
        """Tests :meth:check_files if no "file" form parameter present..
        """
        request_files = MultiDict([
            ('no_file', self.mock_file),
        ])
        files, err = check_files(request_files, None)
        self.assertIsInstance(err, str)
        self.assertTrue(len(err) > 0)

    def test_check_files_filenames(self):
        """Tests :meth:check_files if all files have a filename.
        """
        request_files = MultiDict([
            ('file', self.mock_file),
        ])
        files, err = check_files(request_files, None)
        self.assertIsNone(err)

    def test_check_files_no_filenames(self):
        """Tests :meth:check_files if a file has no filename.
        """
        request_files = MultiDict([
            ('file', MockFileType('')),
        ])
        files, err = check_files(request_files, None)
        self.assertIsInstance(err, str)
        self.assertTrue(len(err) > 0)

    def test_allowed_file_exts_success(self):
        """Tests :meth:allowed_file_exts if files have allowed extensions.
        """
        files = [
            MockFileType('A.java'),
            MockFileType('B.zip')
        ]
        res = allowed_file_exts(files, ['java', 'zip'])
        self.assertTrue(res)

    def test_allowed_file_exts_failure(self):
        """Tests :meth:allowed_file_exts if a file with not allowed extensions present.
        """
        files = [
            MockFileType('A.java'),
            MockFileType('B.go')
        ]
        res = allowed_file_exts(files, ['java', 'zip'])
        self.assertFalse(res)

    def test_get_file_ext(self):
        """Tests :meth:get_file_extension to get the extension.
        """
        res = get_file_extension('A.java')
        self.assertEqual(res, 'java')

    def test_run_cmd(self):
        """Tests :meth:run_cmd if executing a command.
        """
        stdout, stderr = run_cmd(['echo', 'Hello World'])
        self.assertEqual(stdout, 'Hello World')
