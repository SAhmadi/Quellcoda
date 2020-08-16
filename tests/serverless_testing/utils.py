import os

# Globals
ROOT_TEST_DIR = '/app/tests/serverless_testing/'

CONTENT_TYPE_PLAIN = 'text/plain'
CONTENT_TYPE_FORM_DATA = 'multipart/form-data'
CONTENT_TYPE_ZIP = 'application/zip'
CONTENT_TYPE_JSON = 'application/json'

# Filenames and paths for testing
MAIN_FILENAME = 'MyMainClass.java'
MAIN_PATH = os.path.join(ROOT_TEST_DIR, 'multiple_java_files', MAIN_FILENAME)

CALC_FILENAME = 'Calculator.java'
CALC_PATH = os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_FILENAME)

CALC_TEST_FILENAME = 'CalculatorTest.java'
CALC_TEST_PATH = os.path.join(ROOT_TEST_DIR, 'multiple_java_files', CALC_TEST_FILENAME)

GRADLE_PROJECT_FILENAME = 'gradle_project.zip'
GRADLE_PROJECT_PATH = os.path.join(ROOT_TEST_DIR, 'gradle_project', GRADLE_PROJECT_FILENAME)