import json
import urllib
import uuid

import wtforms
from flask import render_template, url_for, request, redirect, jsonify
from werkzeug import MultiDict

from . import ingest
from . import forms
import app
from .. import listObjects
from . import fmQuery
from . import ingest


@ingest.route('/',methods=['GET','POST'])
@ingest.route('/index',methods=['GET','POST'])
def index():
	print('hooo')
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

@ingest.route('/status',methods=['GET','POST'])
def status():
	status = 'form submitted ok'
	print(status)

	try:
		_data = request.form.to_dict(flat=False)
		user = request.form['user']

		if not user in app.app_config['KNOWN_USERS']:
			return render_template('RSerror.html',user=user)

		results = {}
		toIngest =[]
		targetPaths = []
		doProresYES = []
		proresToDaveYES = []
		doConcatYES =[]
		for key, value in _data.items():
			# get names/paths of files we actually want to process
			if 'runIngest' in key:
				toIngest.append(key.replace('runIngest-',''))
			elif 'targetPath' in key:
				targetPaths.append(value[0])
			elif 'doProres' in key:
				doProresYES.append(key.replace('doProres-',''))
			elif 'proresToDave' in key:
				proresToDaveYES.append(key.replace('proresToDave-',''))
			elif 'doConcat' in key:
				doConcatYES.append(key.replace('doConcat-',''))

		for _object in toIngest:
			# build a dict of files:options
			for path in targetPaths:
				if _object in path:
					results[path] = {'basename' : _object}
		# add boolean options to dict
		for path,sub in results.items():
			if results[path]['basename'] in doProresYES:
				results[path]['prores'] = 'True'
			if results[path]['basename'] in proresToDaveYES:
				results[path]['mezzanine to Dave'] = 'True'
			if results[path]['basename'] in doConcatYES:
				results[path]['concat reels'] = 'True'

		for thing, opts in results.items():
			idNumber = ingest.get_acc_from_filename(thing['basename'])
			xml = fmQuery.xml_query(idNumber)
			print(xml)


	except:
		_data = "no data"
		user = "no user"
		toIngest = []
		results = {}

	return render_template(
		'status.html',title='Ingest',
		data=_data,
		user=user,
		toIngest=toIngest,
		results=results
		)
