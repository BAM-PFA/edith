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

	# for k,v in choices.items():
	# 	print(k)
	# 	for value in v.data.items():
	# 		print(value)

	form = forms.IngestForm()
	form.suchChoices = choices

	if form.is_submitted():
		print("HEY")
		result = form.suchChoices
		# print(result)
		suchDict = {}
		for inputObject,_objectForm in result.items():
			subDict = {}
			for fieldname,value in _objectForm.data.items():
				subDict[fieldname] = value
			for fieldname,value in subDict.items():
				iterID = subDict['targetBase']
				uniqueField = fieldname+'-'+iterID
				form.uniqueField = value
			suchDict[inputObject] = subDict

		for k,v in suchDict.items():
			print(k)
			print(v)

		form.jsonResult = json.dumps(suchDict)

		##########################################################
		# OK I THINK THIS IS ANOTHER ROUTE TO EXPLORE:
		# PASS THE VALUES DICT AS A QUERY STRING.
		# NOT WORKING IN THIS VERSION, BUT... MAYBE USEFUL?
		query = urllib.parse.quote_plus(json.dumps(suchDict))
		# # print(query)

		if request.method == 'POST':
			print('POSTed')
			return redirect(url_for('moar', query_string=query))

	return render_template('index.html',title='Index',objects=objects,form=form)

@app.route('/moar/<string:query_string>',methods=['GET','POST'])
def moar(query_string):
	print('MOAR')
	# print(query_string)
	stuff = urllib.parse.unquote_plus(query_string)

	return render_template('moar.html',title='Moar',info=stuff)

@app.route('/status',methods=['GET','POST'])
def status():
	status = 'OK'
	print(status)
	print(request.form.to_dict(flat=False))

	try:
		items = 'stuff'
		data = request.form.data
		# print(data)
		extra = 'bla bla bla'
	except:
		data = "no data"
		extra = ":("
		items = "bloop bloop"
		# print(data)
	return render_template('status.html',title='Ingest',data=data,extra=extra)

	