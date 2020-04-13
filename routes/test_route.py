from flask import Blueprint

test_path_blueprint = Blueprint('tests', __name__)


@test_path_blueprint.route('/', methods=['POST'])
def index():
    return 'Hello from tests'