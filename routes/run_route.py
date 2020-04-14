import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

from flask import Blueprint, request, Response, jsonify
from werkzeug.utils import secure_filename

from globals import JUNIT_PATH
from utils.utils import check_files, run_cmd

run_path_blueprint = Blueprint('run', __name__)


@run_path_blueprint.route('/java', methods=['POST'])
def run_multiple_java_files():
    files, err_resp = check_files(request.files)
    if err_resp is not None:
        return err_resp

    # Get main_file form param
    main_file = request.form.get('main_file', type=str)
    if main_file is None:
        return Response('Error: "main_file" parameter not set!')
    main_file = main_file.rsplit('.')[0]  # Remove possible .java extension

    # Only allow .java files
    for f in files:
        _, ext = os.path.splitext(f.filename)
        ext = ext.lstrip('.')
        if ext != 'java':
            return Response('Error: Route /run/java only accepts .java files!', status=400)

    result = ''
    with tempfile.TemporaryDirectory() as workdir:
        for f in files:
            f.save(os.path.join(workdir, f.filename))

        out_path = os.path.join(workdir, 'out')

        # Run: which javac
        javac_path, _ = run_cmd(['which', 'javac'])
        javac_path = javac_path.rsplit('\n')[0]
        if javac_path == '':  # when 'which javac' doesnt return path of javac
            return Response('Error: javac not found!', status=500)

        # Run: path/to/javac workdir/*.java
        compile_parts = [javac_path, '-d', out_path]
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

        # Run: path/to/java -cp out_path main_file
        java_result, err = run_cmd([java_path, '-cp', out_path, main_file], check_stderr=True)
        if err is not None:
            return Response('Error: ' + err, status=500)

        result = java_result

    return jsonify(output=result)


@run_path_blueprint.route('/gradle', methods=['POST'])
def run_gradle():
    files, err_resp = check_files(request.files)
    if err_resp is not None:
        return err_resp

    # Only allow one zip file and additional jar file
    zip_file = None
    for f in files:
        _, ext = os.path.splitext(f.filename)
        ext = ext.lstrip('.')

        if ext == 'zip' and zip_file is None:
            zip_file = f
        elif ext == 'zip' and zip_file is not None:
            # Multiple zip files not allowed
            return Response('Error: Route /run/gradle only accepts one zip files!')

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

        # Extraction from prev step can contain temp files
        print('files:', str(files))
        print('dirs:', str(dirs))

        for d in dirs:
            if d == '__MACOSX':
                shutil.rmtree(os.path.join(workdir, d))

        # Get project root dir
        project_dir = dirs[0]

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

        # Run: workdir/project_dir/gradlew wrapper --gradle-distribution-url=/app/gradle-6.3-bin.zip
        _, err = run_cmd([os.path.join(workdir, project_dir, 'gradlew'),
                          'wrapper',
                          '--gradle-distribution-url=/app/gradle-6.3-bin.zip'],
                         check_stderr=True)

        if err is not None:
            return Response('Error: ' + err, status=500)

        # Run: workdir/project_dir/gradlew run
        gradlew_result, err = run_cmd([os.path.join(workdir, project_dir, 'gradlew'), 'run'],
                                      check_stderr=True)
        if err is not None:
            return Response('Error: ' + err, status=500)

        result = gradlew_result

    return jsonify(output=result)
