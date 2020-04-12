import tempfile
from flask import Blueprint, request, Response
from utils.utils import check_files

run_path_blueprint = Blueprint('run', __name__, )


@run_path_blueprint.route('/', methods=['POST'])
def index():
    return 'Hello from run'



