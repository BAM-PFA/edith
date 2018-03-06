from flask import Flask

# local imports
from config import app_config

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')

	from .ingest import ingest as ingest_blueprint
	app.register_blueprint(ingest_blueprint)

	return app
