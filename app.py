from flask import Flask
from blueprints.serverless_testing.views import serverless_testing_bp
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(serverless_testing_bp)
CORS(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
