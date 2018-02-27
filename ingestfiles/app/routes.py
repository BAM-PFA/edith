from app import app, listObjects, forms
from flask import render_template, url_for, request, redirect
import wtforms,uuid,json
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
	# for path,_object in objects.items():
	# 	setattr(form,_object,'')
	# 	form._object = wtforms.FormField(forms.ObjectForm(targetPath=path,targetBase=_object))

	result = form.suchChoices
	suchDict = {}
	for k,v in result.items():
		subDict = {}
		for a,b in v.data.items():
			subDict[a] = json.dumps(b)
		suchDict[k] = subDict

	# print(suchDict)
	form.jsonResult = json.dumps(suchDict)
	# print(form.jsonResult)

	if form.is_submitted():
		# print("HEY")
		# result = form.suchChoices
		# suchDict = {}
		# for k,v in result.items():
		# 	subDict = {}
		# 	for a,b in v.data.items():
		# 		subDict[a] = json.dumps(b)
		# 	suchDict[k] = subDict

		# # print(suchDict)
		# form.jsonResult = json.dumps(suchDict)
		# print(form.jsonResult)
		if request.method == 'POST':
			print('POSTed')
			if form.validate_on_submit():
				print("HOOO")
				print(form.jsonResult)
				return redirect(url_for('status'), code=307)

			else:
				print(form.errors)

	return render_template('index.html',title='Index',objects=objects,form=form)

@app.route('/status',methods=['GET','POST'])
def status():
	status = 'OK'
	print(status)
	# print(request.values)
	# print(request.values.to_dict(flat=False))
	# for k,v in request.values.items():
	# 	print(k)
	# 	print(v)
	try:
		items = 'stuff'
		# data = request.values
		data = request.args.get('jsonResult')
		print(items)
		print(data)
		extra = 'LKWELKLN'
		# print(data)
	except:
		data = "no data"
		extra = ":("
		items = "POPOP"
		# print(data)
	return render_template('status.html',title='Ingest',data=data,extra=extra)

	