from app import app, listObjects, forms
from flask import render_template, url_for, request, redirect
import wtforms,uuid
from werkzeug import MultiDict

@app.route('/')#,methods=['GET','POST'])
@app.route('/index')#,methods=['GET','POST'])
def index():
	DIR = app.config["SHARED_DIR"] 
	objects = listObjects.list_objects()
	
	class OneObject(forms.ObjectForm):
		# http://wtforms.simplecodes.com/docs/1.0.1/specific_problems.html
		pass
	choices = {}

	for path,_object in objects.items():
		choices[path] = OneObject(targetPath=path,targetBase=_object)

	# print(choices)
	for item,val in choices.items():
		# set uuid to make sure each instance is unique... for testing only
		setattr(val,'uuid',str(uuid.uuid4()))
		# print(val.uuid)
		# print(val)

	# setattr(forms.IngestForm,'choicesDict',choices)
	form = forms.IngestForm()
	form.choicesDict = choices

	# print(form.choicesDict)

	if form.is_submitted():
		print("HEY")
		result = form.data
		print(result)
		# for key, value in result.items():
		# 	print(key)
		# 	print(value.data)

		return redirect(url_for('status'))
	return render_template('index.html',title='Index',objects=objects,form=form)

@app.route('/status',methods=['GET','POST'])
def status():
	status = 'OK'
	print(status)
	try:
		items = 'stuff'
		# data = request.form.to_dict(flat=False)
		# extra = form.targetObject.data
		data = request.args
		extra = 'LKWELKLN'
		# print(data)
	except:
		data = "no data"
		extra = ":("
		items = "POPOP"
		# print(data)
	return render_template('status.html',title='Ingest',data=data,extra=extra)

	