import os
import tempfile
import zipfile

from flask import Blueprint, request, Response
from werkzeug.utils import secure_filename

from globals import JUNIT_PATH, GRADLE_DIST_FLAG
from utils.utils import check_files, run_cmd

test_path_blueprint = Blueprint('test', __name__)


@test_path_blueprint.route('/java', methods=['POST'])
def test_multiple_java_files():
    files, err_resp = check_files(request.files)
    if err_resp is not None:
        return err_resp

    # Only allow .java files
    for f in files:
        _, ext = os.path.splitext(f.filename)
        ext = ext.lstrip('.')
        if ext != 'java':
            return Response('Error: Route /test/java only accepts .java files!', status=400)

    result = ''
    with tempfile.TemporaryDirectory() as workdir:
        for f in files:
            f.save(os.path.join(workdir, f.filename))

        out_path = os.path.join(workdir, 'out')
        class_path = out_path + ':' + JUNIT_PATH

        # Run: which javac
        javac_path, _ = run_cmd(['which', 'javac'])
        javac_path = javac_path.rsplit('\n')[0]
        if javac_path == '':  # when 'which javac' doesnt return path of javac
            return Response('Error: javac not found!', status=500)

        # Run: path/to/javac -cp workdir:path/to/junit.jar workdir/*.java
        compile_parts = [javac_path, '-d', out_path, '-cp', class_path]
        for f in files:
            compile_parts.append(os.path.join(workdir, f.filename))

        javac_result, _ = run_cmd(compile_parts)
        if javac_result != '':
            return Response('Error: ' + javac_result, status=500)

        # Run: which java
        java_path, _ = run_cmd(['which', 'java'])
        java_path = java_path.rsplit('\n')[0]
        if java_path == '':  # when 'which java' doesnt return path of java
            return Response('Error: java not found!', status=500)

        # Run: path/to/java -jar path/to/junit.jar -cp out_path --scan-class-path
        java_result, err = run_cmd([java_path, '-jar', JUNIT_PATH, '-cp', out_path, '--scan-class-path'],
                                   check_stderr=True)
        if err is not None:
            return Response('Error: ' + err, status=500)

        result = java_result

    # Remove color codes from Junit response
    result = result.replace('[36m', '')
    result = result.replace('[0m', '')
    result = result.replace('[34m', '')
    result = result.replace('[32m', '')
    result = result.replace('[31m', '')
    # return jsonify(output=result)
    return Response(result, status=200)


@test_path_blueprint.route('/gradle', methods=['POST'])
def test_gradle():
    files, err_resp = check_files(request.files)
    if err_resp is not None:
        return err_resp

    # Only allow one zip file and additional jar file
    zip_file = None
    for f in files:
        _, ext = os.path.splitext(f.filename)
        ext = ext.lstrip('.')

        if ext.lower() == 'zip' and zip_file is None:
            zip_file = f
        elif ext.lower() == 'zip' and zip_file is not None:
            # Multiple zip files not allowed
            return Response('Error: Route /run/gradle only accepts one zip file!')

        if ext.lstrip('.').lower() != 'zip' and ext.lstrip('.').lower() != 'jar':
            return Response('Error: Route /run/gradle only accepts one .zip file and additional .jar files!',
                            status=400)

    result = ''
    with tempfile.TemporaryDirectory() as workdir:
        # Extract zip file
        filename = secure_filename(zip_file.filename)
        zip_file.save(os.path.join(workdir, filename))
        zip_file = zipfile.ZipFile(os.path.join(workdir, filename), 'r')
        zip_file.extractall(path=workdir)
        zip_file.close()
        os.remove(os.path.join(workdir, filename))

        # Read all files in workdir
        files = [f for f in os.listdir(workdir) if os.path.isfile(os.path.join(workdir, f))]
        dirs = [f for f in os.listdir(workdir) if os.path.isdir(os.path.join(workdir, f))]

        clean_dirs = [d for d in dirs if not d.startswith('_') and not d.startswith('.')]

        # Get project root dir
        project_dir = clean_dirs[0]

        # Give permission to change project dir
        _, err = run_cmd(['chmod', '+rwx', os.path.join(workdir, project_dir)],
                         check_stderr=True)
        if err is not None:
            return Response('Error:' + err, status=500)

        # Give permission to execute gradlew
        _, err = run_cmd(['chmod', '+x', os.path.join(workdir, project_dir, 'gradlew')],
                         check_stderr=True)
        if err is not None:
            return Response('Error: ' + err, status=500)

        # Run: cd path/to/workdir
        os.chdir((os.path.join(workdir, project_dir)))

        # Run: workdir/project_dir/gradlew wrapper --gradle-distribution-url=GRADLE_DIST_FLAG
        _, err = run_cmd([os.path.join(workdir, project_dir, 'gradlew'),
                          'wrapper',
                          GRADLE_DIST_FLAG],
                         check_stderr=True)

        if err is not None:
            return Response('Error: ' + err, status=500)

        # Run: workdir/project_dir/gradlew test
        gradlew_result, err = run_cmd([os.path.join(workdir, project_dir, 'gradlew'), 'test'],
                                      check_stderr=True)
        if err is not None:
            return Response('Error: ' + err, status=500)

        result = gradlew_result

    # Remove color codes from Junit response
    result = result.replace('[36m', '')
    result = result.replace('[0m', '')
    result = result.replace('[34m', '')
    result = result.replace('[32m', '')
    result = result.replace('[31m', '')
    # return jsonify(output=result)
    return Response(result, status=200)