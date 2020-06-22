import os
import subprocess
from typing import Tuple, Optional, List
from werkzeug.datastructures import MultiDict

# GLOBALS
JAVAC_PATH = '/usr/lib/jvm/default-jvm/bin/javac'
JAVA_PATH = '/usr/lib/jvm/default-jvm/bin/java'
JUNIT_PATH = '/app/junit-platform-console-standalone-1.6.2.jar'
GRADLE_PATH = '/app/gradle-6.3/bin/gradle'


def check_files(request_files: MultiDict,
                allowed_extensions: Optional[List[str]]) -> Tuple[Optional[MultiDict], Optional[str]]:
    """Checks if files are present and valid.

    :param request_files: The file(s) send with the request.
    :type request_files: MultiDict
    :param allowed_extensions: Allowed file-extensions
    :type allowed_extensions: List[str]

    :return: The files and error response
    :rtype: Tuple[Optional[MultiDict], Optional[str]]
    """
    # Check if at least one file was send with the request
    if 'file' not in request_files:
        return None, 'No files(s) provided!'

    files = request_files.getlist('file')

    # Check if all files have a filename
    for f in files:
        if f.filename == '':
            return None, 'File has no name!'

    # Only allow files with valid `extensions`
    if allowed_extensions is not None:
        if not allowed_file_extensions(files, allowed_extensions):
            return None, 'Only {0} file extensions allowed!'.format(str(allowed_extensions))

    # Otherwise files are valid
    return files, None


def allowed_file_extensions(files: List, extensions: List[str]) -> bool:
    """Checks if all files have one of the allowed `extensions`.

    :param files: List of files send with the request.
    :type files: List
    :param extensions: Allowed file extensions.
    :type extensions: List[str]

    :return: Returns true if files have a valid extension.
    :rtype: bool
    """
    for f in files:
        ext = get_file_extension(f.filename)
        if ext not in extensions:
            return False
    return True


def get_file_extension(filename: str) -> str:
    """Gets the file extension from a filename.

    :param filename: The filename of the file.
    :type filename: str

    :return: The extension of the file.
    :rtype: str
    """
    _, ext = os.path.splitext(filename)
    ext = ext.lstrip('.')
    return ext


def run_cmd(cmd: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """Run command and possibly capture stdout and stderr
    and flatten them to strings.

    :param cmd: The command parts to run.
    :type cmd: List[str]

    :return: A tuple with
    :rtype: Tuple[Optional[str], Optional[str]]
    """
    cmd_out = subprocess.run(cmd, capture_output=True)

    stdout = None
    stderr = None
    if cmd_out.stdout != b'':
        stdout = cmd_out.stdout.decode().strip()
    if cmd_out.stderr != b'':
        stderr = cmd_out.stderr.decode().strip()

    return stdout, stderr
