import os
import tempfile
from typing import Tuple, Union
from flask import Blueprint, Response, request, Request, jsonify, render_template

from .exec_types.compile import javac
from .exec_types.exec_types import ExecType
from .exec_types.execute import java
from .helpers import check_files, run_cmd, JUNIT_PATH, get_file_extension, GRADLE_PATH, \
    extract_zip

serverless_testing_bp = Blueprint('serverless_testing', __name__)


@serverless_testing_bp.route('/', methods=['GET'])
def index():
    """Route to the index.html file. This file loosely implements
    the MOPS layout.
    :return: The index.html file
    """
    return render_template('index.html',
                           name='Serverless Editor',
                           title='Serverless Editor',
                           headcontent=True,
                           navigation=True,
                           bodycontent=True, )


@serverless_testing_bp.route('/run/java', methods=['POST'])
def run_java_files() -> Response:
    """Route to compile and run java files.

    :return: The stdout of the java program.
    :rtype: Response
    """
    resp = execute_java(request, exec_type=ExecType.run)
    return resp


@serverless_testing_bp.route('/run/gradle', methods=['POST'])
def run_gradle() -> Union[Response, Tuple[Response, int]]:
    """Route to run a gradle program.

    :return: The stdout of the gradle program.
    :rtype: Union[Response, Tuple[Response, int]]
    """
    resp = execute_gradle(request, exec_type=ExecType.run)
    return resp


@serverless_testing_bp.route('/test/java', methods=['POST'])
def test_java_files() -> Response:
    """Route to compile and test java files.

    :return: The test result.
    :rtype: Response
    """
    resp = execute_java(request, exec_type=ExecType.test)
    return resp


@serverless_testing_bp.route('/test/gradle', methods=['POST'])
def test_gradle() -> Union[Response, Tuple[Response, int]]:
    """Route to test a gradle program.

    :return: The test result.
    :rtype: Union[Response, Tuple[Response, int]]
    """
    resp = execute_gradle(request, exec_type=ExecType.test)
    return resp


def execute_java(req: Request, exec_type: ExecType) -> Response:
    """Compiles ands executes java files. The "exec_type" denotes if
    files should be run or tested.

    :param req: The request object.
    :type req: Request
    :param exec_type: Decides if files should be run or tested.
    :type exec_type: ExecType

    :return: The java program stdout or stderr and status code.
    :rtype: Response
    """
    assert exec_type == ExecType.run or exec_type == ExecType.test, '[exec_type] can only be run or test'

    # Check if files are present and valid
    files, err = check_files(req.files, allowed_ext=['java'])
    if err is not None:
        return Response(err, status=400)

    # Get main_file from form parameters, needed for /run java command
    main_file = None
    if exec_type == ExecType.run:
        main_file = req.form.get('main_file', type=str)
        if main_file is not None:
            main_file = main_file.rsplit('.', maxsplit=1)[0]
        else:
            return Response('Form parameter [main_file] is missing!', status=400)

    # Compile and run or test files
    with tempfile.TemporaryDirectory() as work_path:
        for f in files:
            f.save(os.path.join(work_path, f.filename))

        out_path = os.path.join(work_path, 'out')
        class_path = out_path + ':' + JUNIT_PATH
        file_paths = [os.path.join(work_path, f.filename) for f in files]

        # Compile java files
        stdout, stderr = javac(file_paths=file_paths,
                               out_path=out_path,
                               class_path=class_path)
        if stdout is not None:
            return Response(stdout, status=500)
        elif stderr is not None:
            return Response(stderr, status=500)

        # Execute compiled java files
        result, err = java(exec_type=exec_type,
                           class_path=class_path,  # out_path
                           main_file=main_file)
        if err is not None:
            return Response(err, status=500)

    return Response(result, status=200)


def execute_gradle(req: Request, exec_type: ExecType) -> Union[Response, Tuple[Response, int]]:
    """Run or test a gradle project. The "exec_type" denotes if
    files gradle project should be run (with gradle run) or tested with (gradle test).

    :param req: The request object.
    :type req: Request
    :param exec_type: Decides if zip should be run or tested.
    :type exec_type: ExecType

    :return: The gradle project stdout or stderr and status code as json or text/html.
    :rtype: Union[Response, Tuple[Response, int]]
    """
    assert exec_type == ExecType.run or exec_type == ExecType.test,\
        '[exec_type] can only be run or test'

    # Check if files are present and valid
    files, err = check_files(req.files, allowed_ext=['zip'])
    if err is not None:
        return jsonify(error=err), 400

    # Get the zip file
    zip_file = None
    for f in files:
        if get_file_extension(f.filename).lower() == 'zip':
            zip_file = f

    # Run or test gradle project
    with tempfile.TemporaryDirectory() as work_path:
        extract_zip(zip_file, dest=work_path)

        # Read all files in work_path
        dirs = [d for d in os.listdir(work_path) if os.path.isdir(os.path.join(work_path, d))]

        # Filter out possible temp files from previous extraction
        clean_dirs = [d for d in dirs if not d.startswith('_') and not d.startswith('.')]

        # Only project root dir left
        project_dir = clean_dirs[0]

        # Run: cd work_path/project_root
        os.chdir(os.path.join(work_path, project_dir))

        run_or_test = 'run' if exec_type == ExecType.run else 'test'
        gradle_stdout, err = run_cmd([GRADLE_PATH, run_or_test, '--console=plain'])
        if err is not None:
            return jsonify(error=err), 500

        result = gradle_stdout

    if request.args.get('return') == 'json':
        # Returns json if ?return=json query param added, primarily for frontend
        return jsonify(msg=result), 200
    else:
        return Response(result, status=200)
