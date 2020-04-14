# Utility functions
# Contains useful utility functions used in multiple files

import os
import subprocess
import sys

from flask import Response
from typing import Optional, Tuple, List
from werkzeug.datastructures import MultiDict

from globals import ALLOWED_EXTENSIONS


def check_files(request_files: MultiDict) -> Tuple[Optional[MultiDict], Optional[Response]]:
    """Checks if file(s) were send with the request. Also checks if they
    have a filename and contain one of the allowed file extensions.

    :param request_files: The file(s) send with the request.
    :return: A :class:`Optional[Response]` if file(s) are invalid.
    """

    # Check if at least one file was send with the request
    if not files_present(request_files):
        return None, Response('No file(s) provided!', status=400)

    files = request_files.getlist('file')

    # Check if all files have a filename
    if not valid_filename(files):
        return None, Response('Error: File has no name!', status=400)

    # Check if the file extensions are allowed
    # if not allowed_file_extension(files):
    #    return None, Response('Error: Only .java and .zip files allowed!', status=400)

    # Otherwise files are valid
    return files, None


def files_present(request_files: MultiDict) -> bool:
    if 'file' not in request_files:
        return False
    return True


def valid_filename(request_files: List) -> bool:
    for f in request_files:
        if f.filename == '':
            return False
    return True


def allowed_file_extension(files: MultiDict) -> bool:
    """Inspects the file-extensions of `files`.
    Only allows extensions inside `ALLOWED_EXTENSIONS`

    :param files:
    :return: Result whether all file-extensions in `files` are allowed
    """
    for f in files:
        _, ext = os.path.splitext(f.filename)
        ext = ext.lstrip('.')
        if ext not in ALLOWED_EXTENSIONS:
            return False
    return True


def run_cmd(cmd_list: List[str],
            check_stdout: bool = False,
            check_stderr: bool = False) -> Tuple[Optional[str], Optional[str]]:
    """ """

    cmd_instance = subprocess.run(cmd_list, capture_output=True)
    if check_stdout:
        if cmd_instance.stdout != b'':
            return None, cmd_instance.stdout.decode()
    if check_stderr:
        if cmd_instance.stderr != b'':
            return None, cmd_instance.stderr.decode()

    cmd_resp = cmd_instance.stdout.decode()

    return cmd_resp, None
