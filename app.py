from flask_cors import CORS
from blueprints import blueprints
from flask_smorest import Api
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from geolite.geolitedb import Geolite
import logging
import os

# Get environment variables
MY_PORT = os.environ.get('MY_PORT') or 10106
GEOLITE_CSV_LOCATION = os.environ.get('GEOLITE_CSV_LOCATION') or 'db/geolite2-city-ipv4.csv'
GEOLITE_CSV_COLUMNS = os.environ.get('GEOLITE_CSV_COLUMNS') or None
LOGLEVEL = os.environ.get('LOGLEVEL') or None
logging.basicConfig()
if LOGLEVEL == 'DEBUG':
    logging.root.setLevel(logging.DEBUG)
if LOGLEVEL == 'INFO':
    logging.root.setLevel(logging.INFO)
if LOGLEVEL == 'ERROR':
    logging.root.setLevel(logging.INFO)

# Config flask
app = Flask(__name__)

app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['API_TITLE'] = 'coordinate system'
app.config['API_VERSION'] = 'v1'
app.config["OPENAPI_URL_PREFIX"] = '/docs'

api = Api(app, spec_kwargs={"host": "oakestra.io", "x-internal-id": "1"})
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Register apis
for bp in blueprints:
    api.register_blueprint(bp)

# Swagger docs
SWAGGER_URL = '/api/docs'
API_URL = '/docs/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "coordinate system"
    },
)
app.register_blueprint(swaggerui_blueprint)

# init geolite
Geolite(location=GEOLITE_CSV_LOCATION, columns=GEOLITE_CSV_COLUMNS)
