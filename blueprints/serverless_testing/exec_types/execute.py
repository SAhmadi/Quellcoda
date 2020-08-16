from typing import Optional, Tuple

from blueprints.serverless_testing.exec_types.exec_types import ExecType
from blueprints.serverless_testing.helpers import run_cmd, JAVA_PATH, JUNIT_PATH


def java(exec_type: ExecType,
         class_path: str,
         main_file: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Runs or tests compiled java class files inside "path".
    The "execution_type" denotes running or testing the java files.
    The "main_file" is needed to run the java files.

    :param exec_type: Decides to run or test the files.
    :type exec_type: ExecType
    :param class_path: The path to look for the compiled class files.
    :type class_path: str
    :param main_file: Name of the java file with the main method.
    :type main_file: Optional[str]

    :return: The stdout and stderr after java command is called.
    :rtype: Tuple[Optional[str], Optional[str]]:
    """
    assert exec_type == ExecType.run or exec_type == ExecType.test, '[exec_type] can only be run or test'

    if exec_type == ExecType.run and main_file is not None:
        java_stdout, java_stderr = run_cmd([JAVA_PATH, '-cp', class_path, main_file])
    else:
        java_stdout, java_stderr = run_cmd([JAVA_PATH, '-jar', JUNIT_PATH, '-cp', class_path, '--scan-class-path'])

    return java_stdout, java_stderr
