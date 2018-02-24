from ingest import ingest, listObjects, forms
from flask import render_template

@ingest.route('/')
@ingest.route('/index')

def index():
    DIR = ingest.config["SHARED_DIR"] 
    objects = listObjects.list_objects()
    form = forms.ingestForm()
    return render_template('index.html',title='Ingest',objects=objects,form=form)

