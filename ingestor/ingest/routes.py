from ingest import ingest, listObjects
from flask import render_template

@ingest.route('/')
@ingest.route('/index')

def index():
    DIR = ingest.config["SHARED_DIR"] 
    objects = listObjects.list_objects()

    return render_template('index.html',title='Ingest',objects=objects)

