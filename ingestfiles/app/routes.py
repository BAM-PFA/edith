from app import app, listObjects, forms
from flask import render_template, url_for, request, redirect
import wtforms,uuid
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

	# print(choices)
	# for item,val in choices.items():
	# 	print(val)

	# setattr(forms.IngestForm,'choicesDict',choices)
	# setattr(forms.IngestForm(),'suchChoices',choices)

	form = forms.IngestForm()
	form.suchChoices = choices
	form.choicesDict = choices
	for path,_object in objects.items():
		setattr(form,_object,'')
		form._object = wtforms.FormField(forms.ObjectForm(targetPath=path,targetBase=_object))
		# print(form._object.ata)
	# print(form.data)

	if form.is_submitted():
		print("HEY")
		# setattr(form,'suchChoices',choices)
	if request.method == 'POST':
		print('POSTed')
		if form.validate_on_submit():
			result = form.suchChoices
			print("HOOO")
			for k,v in result.items():
				print(k)
				print(v.data)

			return redirect(url_for('status'))
		else:
			print(form.errors)
	return render_template('index.html',title='Index',objects=objects,form=form)

@app.route('/status',methods=['GET','POST'])
def status():
	status = 'OK'
	print(status)
	try:
		items = 'stuff'
		# data = request.form.to_dict(flat=False)
		# extra = form.targetObject.data
		data = request
		extra = 'LKWELKLN'
		# print(data)
	except:
		data = "no data"
		extra = ":("
		items = "POPOP"
		# print(data)
	return render_template('status.html',title='Ingest',data=data,extra=extra)

	