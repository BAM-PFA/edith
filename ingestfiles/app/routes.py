from app import app, listObjects, forms
from flask import render_template, url_for, request, redirect, jsonify
import wtforms,uuid,json, urllib
from werkzeug import MultiDict

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
	DIR = app.config["SHARED_DIR"] 
	objects = listObjects.list_objects()
	
	class OneObject(forms.ObjectForm):
		# http://wtforms.simplecodes.com/docs/1.0.1/specific_problems.html
		pass
	choices = {}

	for path,_object in objects.items():
		choices[path] = OneObject(targetPath=path,targetBase=_object)

	form = forms.IngestForm()
	form.suchChoices = choices

	return render_template('index.html',title='Index',objects=objects,form=form)

@app.route('/status',methods=['GET','POST'])
def status():
	status = 'form submitted ok'
	print(status)

	try:
		data = request.form.to_dict(flat=False)
		toIngest = []
		for key, value in data.items():
			if 'runIngest' in key:
				toIngest.append(key.replace('runIngest-',''))
		# print(data)
	except:
		data = "no data"

	return render_template('status.html',title='Ingest',data=data,toIngest=toIngest)

	