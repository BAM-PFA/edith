from flask import Blueprint

ingest = Blueprint('ingest', __name__)

from . import views