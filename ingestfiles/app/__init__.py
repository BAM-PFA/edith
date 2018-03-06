from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')
	db.init_app(app)

	from .ingest import ingest as ingest_blueprint
	app.register_blueprint(ingest_blueprint)


	return app


# from app import routes
