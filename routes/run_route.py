from flask import Blueprint

run_path_blueprint = Blueprint('run', __name__)


@run_path_blueprint.route('/', methods=['POST'])
def index():
    return 'Hello from run'



