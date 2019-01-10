#!/usr/bin/env python3
# standard library modules
import re
# non-standard libraries
from flask import render_template, request, flash, url_for
from flask_login import login_required, current_user
import wtforms
# local modules
import app
from . import ingest
from . import ingestProcesses
from . import fmQuery
from . import forms

from .. import db
from .. models import User

from .. import listObjects

@ingest.route('/ingest_stuff',methods=['GET','POST'])
@login_required
def ingest_stuff():
	# `objects` is a dict of {fullpath:basename} pairs
	objects = listObjects.list_objects('shared')

	class OneObject(forms.ObjectForm):
		# http://wtforms.simplecodes.com/docs/1.0.1/specific_problems.html
		pass
	choices = {}

	for path,_object in objects.items():
		choices[path] = OneObject(targetPath=path,targetBase=_object)

	form = forms.IngestForm()
	form.suchChoices = choices

	return render_template(
		'ingest/ingest.html',
		title='EDITH',
		objects=objects,
		form=form
		)

@ingest.route('/status',methods=['GET','POST'])
@login_required
def status():
	status = 'form submitted ok'
	error = None
	print(status)
	
	_data = request.form.to_dict(flat=False)
	print(_data)

	results = {}
	toIngest =[]
	targetPaths = []
	doProresYES = []
	proresToDaveYES = []
	doConcatYES =[]
	metadataEntries = {}

	for key, value in _data.items():
		# get names/paths of files we actually want to process
		if 'runIngest' in key:
			toIngest.append(key.replace('runIngest-',''))
		# targetPath is the path of the item coming from the form
		elif 'targetPath' in key:
			targetPaths.append(value[0])
		elif 'doProres' in key:
			doProresYES.append(key.replace('doProres-',''))
		elif 'proresToDave' in key:
			proresToDaveYES.append(key.replace('proresToDave-',''))
		elif 'doConcat' in key:
			doConcatYES.append(key.replace('doConcat-',''))
		# elif 'metadataSource' in key:
		# 	doConcatYES.append(key.replace('doConcat-',''))
		# start trawling for metadata entries
		elif 'metadataForm' in key:
			# print(key)
			# get the field label and object via regex
			pattern = r'(metadataForm-)([a-zA-Z0-9_]+)(-)(.*)'
			fieldSearch = re.search(pattern,key)
			# raw fields are formed as userMD_1_eventLocation
			# field = fieldSearch.group(2).replace('userMD_','')
			field = re.sub(r"(userMD_)(\d)(_)", '', fieldSearch.group(2))
			theObject = fieldSearch.group(4)
			# print(field,theObject)
			if not theObject in  metadataEntries:
				metadataEntries[theObject] = {}
				# `value` here is returned as a list from the metadata FormField
				metadataEntries[theObject][field] = value[0]
			else:
				metadataEntries[theObject][field] = value[0]

	for _object in toIngest:
		# build a dict of files:options
		for path in targetPaths:
			# this line is probably fucking something up (duplicating calls for similar named files) @fixme
			if _object in path:
				results[path] = {'basename' : _object}
				if _object in metadataEntries:
					results[path]['userMetadata'] = metadataEntries[_object]

	# add boolean options to dict
	for path,sub in results.items():
		if results[path]['basename'] in doProresYES:
			results[path]['prores'] = 'True'
		if results[path]['basename'] in proresToDaveYES:
			results[path]['mezzanine to Dave'] = 'True'
		if results[path]['basename'] in doConcatYES:
			results[path]['concat reels'] = 'True'

	try:
		# pass dict of files:options to ingestProcesses.main() and get back
		# a dict that includes metadata
		results = ingestProcesses.main(results)

	except:
		flash("There was an error with your request. Try again. :(")
		_data = _data
		toIngest = toIngest
		results = {}

	return render_template(
		'ingest/status.html',
		title='Ingest',
		data=_data,
		toIngest=toIngest,
		results=results
		)
