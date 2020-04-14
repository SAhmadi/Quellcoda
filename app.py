from flask import Flask

from routes.run_route import run_path_blueprint
from routes.test_route import test_path_blueprint

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(run_path_blueprint, url_prefix='/run')
app.register_blueprint(test_path_blueprint, url_prefix='/test')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
