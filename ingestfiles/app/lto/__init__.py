from flask import Blueprint

lto = Blueprint('lto', __name__)

from . import views