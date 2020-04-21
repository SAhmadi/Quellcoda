import os
import tempfile
import zipfile
from typing import Optional, Tuple

from flask import Blueprint, Response, request, Request, jsonify
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename
from .helpers import check_files, run_cmd, JUNIT_PATH, get_file_extension, GRADLE_PATH, JAVAC_PATH, JAVA_PATH

serverless_testing_bp = Blueprint('serverless_testing', __name__)


@serverless_testing_bp.route('/run/java', methods=['POST'])
def run_java_files() -> Tuple[Response, int]:
    """Route to compile and run java files

    :return: The stdout of the java program.
    :rtype: Tuple[Response, int]
    """
    resp = compile_and_execute_java(request, execution_type='run')
    return resp


@serverless_testing_bp.route('/run/gradle', methods=['POST'])
def run_gradle() -> Tuple[Response, int]:
    """Route to run a gradle program.

    :return: The stdout of the gradle program.
    :rtype: Tuple[Response, int]
    """
    resp = execute_gradle(request, execution_type='run')
    return resp


@serverless_testing_bp.route('/test/java', methods=['POST'])
def test_java_files() -> Tuple[Response, int]:
    """Route to compile and test java files.

    :return: The test result.
    :rtype: Tuple[Response, int]
    """
    resp = compile_and_execute_java(request, execution_type='test')
    return resp


@serverless_testing_bp.route('/test/gradle', methods=['POST'])
def test_gradle() -> Tuple[Response, int]:
    """Route to test a gradle program.

    :return: The test result.
    :rtype: Tuple[Response, int]
    """
    resp = execute_gradle(request, execution_type='test')
    return resp


def compile_java(execution_type: str,
                 files: MultiDict,
                 work_path: str,
                 out_path: str,
                 class_path: str) -> Optional[str]:
    """Compiles java "files" at "work_path" into destination "out_path".
    Adds "class_path" to javac command.

    :param execution_type: Compile files for running or testing request.
    :type execution_type: str
    :param files: The java files to be compiled.
    :type files: MultiDict
    :param work_path: The path the .java files are located.
    :type work_path: str
    :param out_path: The destination path the .class files should be put.
    :type out_path: str
    :param class_path: The class-path to get added to javac command.
    :type class_path: str

    :return: The stdout after javac command.
    :rtype: Optional[str]
    """
    assert execution_type == 'run' or execution_type == 'test', \
        '[execution_type] can only be run or test.'

    if execution_type == 'run':
        # Run: path/to/javac -d out_dir work_dir/*.java
        compile_cmd = [JAVAC_PATH, '-d', out_path]
    else:
        # Run: path/to/javac -cp work_dir:path/to/junit.jar work_dir/*.java
        compile_cmd = [JAVAC_PATH, '-d', out_path, '-cp', class_path]

    [compile_cmd.append(os.path.join(work_path, f.filename)) for f in files]

    javac_stdout, _ = run_cmd(compile_cmd)
    return javac_stdout


def execute_java(execution_type: str,
                 path: str,
                 main_file: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Runs or tests compiled java class files inside "path".
    The "execution_type" denotes running or testing the java files.
    The "main_file" is needed to run the java files.

    :param execution_type: Denotes to run or test the files.
    :type execution_type: str
    :param path: The path the compiled files are located.
    :type path: str
    :param main_file: Name of the java file with the main method.
    :type main_file: Optional[str]

    :return: The stdout and stderr after java command.
    :rtype: Tuple[Optional[str], Optional[str]]
    """
    assert execution_type == 'run' or execution_type == 'test', \
        '[execution_type] can only be run or test.'

    # Run: path/to/java -cp out_dir path/to/main_file
    if execution_type == 'run' and main_file is not None:
        java_stdout, err = run_cmd([JAVA_PATH, '-cp', path, main_file])
    # Run: path/to/java -jar path/to/junit.jar -cp out_dir --scan-class-path
    else:
        java_stdout, err = run_cmd([JAVA_PATH, '-jar', JUNIT_PATH, '-cp', path, '--scan-class-path'])

    return java_stdout, err


def compile_and_execute_java(req: Request, execution_type: str) -> Tuple[Response, int]:
    """Compiles ands executes java files. The "execution_type" denotes
    running or testing the files.

    :param req: The request object.
    :type req: Request
    :param execution_type: Denotes to run or test the files.
    :type execution_type: str

    :return: The java program stdout or stderr and status code.
    :rtype: Tuple[Response, int]
    """
    assert execution_type == 'run' or execution_type == 'test', \
        '[execution_type] can only be run or test.'

    files, err = check_files(req.files, allowed_extensions=['java', 'jar'])
    if err is not None:
        return jsonify(error=err), 400

    # Get main_file from form parameters if running code
    main_file = None
    if execution_type == 'run':
        main_file = req.form.get('main_file', type=str)
        if main_file is None:
            return jsonify(error='Form parameter [main_file] is missing!'), 400

        # Remove possible . (dot) in filename
        main_file = main_file.rsplit('.', maxsplit=1)[0]

    with tempfile.TemporaryDirectory() as work_path:
        for f in files:
            f.save(os.path.join(work_path, f.filename))

        out_path = os.path.join(work_path, 'out')
        class_path = out_path + ':' + JUNIT_PATH

        # Compile java files
        compile_output = compile_java(execution_type=execution_type,
                                      files=files,
                                      work_path=work_path,
                                      out_path=out_path,
                                      class_path=class_path)
        if compile_output is not None:
            return jsonify(error=compile_output), 500

        # Run java files
        result, err = execute_java(execution_type=execution_type,
                                   path=out_path,
                                   main_file=main_file)
        if err is not None:
            return jsonify(error=err), 500

    return jsonify(out=result), 200


def execute_gradle(req: Request, execution_type: str) -> Tuple[Response, int]:
    """Run or test a gradle project. The "execution_type" denotes running or
    testing the gradle project.

    :param req: The request object.
    :type req: Request
    :param execution_type: Denotes to run or test the files.
    :type execution_type: str

    :return: The gradle project stdout or stderr and status code.
    :rtype: Tuple[Response, int]
    """
    assert execution_type == 'run' or execution_type == 'test',\
        '[execution_type] can only be run or test.'

    files, err = check_files(req.files, allowed_extensions=['zip', 'jar'])
    if err is not None:
        return jsonify(error=err), 400

    # Get the zip file
    zip_file = None
    for f in files:
        if get_file_extension(f.filename).lower() == 'zip':
            zip_file = f

    with tempfile.TemporaryDirectory() as work_dir:
        # Extract zip file
        filename = secure_filename(zip_file.filename)
        zip_file.save(os.path.join(work_dir, filename))
        zip_file = zipfile.ZipFile(os.path.join(work_dir, filename), 'r')
        zip_file.extractall(path=work_dir)
        zip_file.close()
        os.remove(os.path.join(work_dir, filename))

        # Read all files in work_dir
        dirs = [f for f in os.listdir(work_dir) if os.path.isdir(os.path.join(work_dir, f))]

        # Extraction from prev step can contain temp files
        clean_dirs = [d for d in dirs if not d.startswith('_') and not d.startswith('.')]

        # Get project root dir
        project_dir = clean_dirs[0]

        # Run: cd path/to/work_dir/project_root
        os.chdir(os.path.join(work_dir, project_dir))

        # Run: GRADLE_PATH run --quiet --console=plain
        gradle_stdout, err = run_cmd([GRADLE_PATH, execution_type, '--console=plain'])
        if err is not None:
            return jsonify(error=err), 500

        result = gradle_stdout

    return jsonify(out=result), 200
