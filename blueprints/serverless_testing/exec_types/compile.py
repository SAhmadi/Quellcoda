from typing import Optional, List, Tuple
from blueprints.serverless_testing.exec_types.exec_types import ExecType
from blueprints.serverless_testing.helpers import JAVAC_PATH, run_cmd


def javac(exec_type: ExecType,
          file_paths: List[str],
          out_path: str,
          class_path: str) -> Tuple[Optional[str], Optional[str]]:
    """Runs javac cmd to compile "files" located at "work_path" and outputs result
    into destination "out_path". Adds "class_path" to javac command.

    :param exec_type: Compile files for running or testing request.
    :type exec_type: ExecType
    :param file_paths: The java file paths to be compiled.
    :type file_paths: List[str]
    :param out_path: The destination path the .class files should be put.
    :type out_path: str
    :param class_path: The class-path to get added to javac command.
    :type class_path: str

    :return: The stdout and stderr after javac command.
    :rtype: Tuple[Optional[str], Optional[str]]
    """
    assert exec_type == ExecType.run or exec_type == ExecType.test, '[exec_type] can only be run or test'

    if exec_type == ExecType.run:
        compile_cmd = [JAVAC_PATH, '-d', out_path]
    else:
        compile_cmd = [JAVAC_PATH, '-d', out_path, '-cp', class_path]

    # Append all java file paths that should be compiled
    for fp in file_paths:
        compile_cmd.append(fp)

    # Final cmd for run should be like:  javac -d out_dir work_dir/*.java
    # Final cmd for test should be like: javac -d out_path -cp work_dir:path/to/junit.jar work_dir/*.java
    javac_stdout, javac_stderr = run_cmd(compile_cmd)

    return javac_stdout, javac_stderr
