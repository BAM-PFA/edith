from flask import Flask
from config import Config

ingest = Flask(__name__)
ingest.config.from_object(Config)

from ingest import routes
