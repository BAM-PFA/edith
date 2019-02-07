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
from .. models import User, Data_Source

from .. import listObjects

@ingest.route('/ingest_stuff',methods=['GET','POST'])
@login_required
def ingest_stuff():
	# `objects` is a dict of {fullpath:basename} pairs
	objects = listObjects.list_objects('shared')

	class OneObject(forms.ObjectForm):
		# init a form that can be instantiated per-object
		# http://wtforms.simplecodes.com/docs/1.0.1/specific_problems.html			
		pass

	choices = {}

	# query the db for the available metadata sources
	# https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield?rq=1
	available_metadataSources = db.session.query(Data_Source).all()
	metadataSource_list = [
		(i.id, i.dbName) for i in available_metadataSources
		]
	# set the default sourceID to `0` which will be handled later
	# as a null value
	# https://stackoverflow.com/questions/46820042/trying-to-insert-blank-option-in-dynamic-wtform-field
	metadataSource_list.insert(0,(0,'Please select a metadata source:'))

	for path,_object in objects.items():
		# this section creates a per-object sub form that is used to 
		# pass the choices for each object
		choices[path] = OneObject(targetPath=path,targetBase=_object)
		choices[path].metadataSource.choices = metadataSource_list
	
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
	# sys.exit

	results = {}
	toIngest =[]
	targetPaths = []
	doProresYES = []
	proresToDaveYES = []
	doConcatYES =[]
	metadataSourceSelection = {}
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
		elif 'metadataSource' in key:
			pattern = r'(metadataSource-)(.*)'
			mySearch = re.search(pattern,key)
			theObject = mySearch.group(2)
			metadataSourceSelection[theObject] = value[0]
		# start trawling for metadata entries
		# skip entries that are blank
		# -> n.b. this should result in no userMetadata dict 
		#    if there isn't any user md
		elif 'metadataForm' in key and not value == ['']:
			# print(key)
			# get the field label and object via regex
			pattern = r'(metadataForm-)([a-zA-Z0-9_]+)(-)(.*)'
			fieldSearch = re.search(pattern,key)
			# raw fields are formed as userMD_1_eventLocation
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
				if _object in metadataSourceSelection:
					results[path]['metadataSource'] = metadataSourceSelection[_object]

	# add boolean options to dict
	for path,sub in results.items():
		if results[path]['basename'] in doProresYES:
			results[path]['prores'] = 'True'
		if results[path]['basename'] in proresToDaveYES:
			results[path]['mezzanine to Dave'] = 'True'
		if results[path]['basename'] in doConcatYES:
			results[path]['concat reels'] = 'True'

	print(results)
	# sys.exit
	# try:
		# pass dict of files:options to ingestProcesses.main() and get back
		# a dict that includes metadata
	results = ingestProcesses.main(results)

	# start building a dict of messages and warnings to display
	# from the results of ingestProcesses.main()
	statusMessages = {}
	for _object, objectOptions in results.items():
		anObject = objectOptions['basename']
		statusMessages[anObject] = {}
		statusMessages[anObject]['Warnings'] = []
		statusMessages[anObject]['Messages'] = []
		for message in objectOptions['ingestStatus']:
			if message.startswith("Warning"):
				statusMessages[anObject]['Warnings'].append(message)
			else:
				statusMessages[anObject]['Messages'].append(message)
		if objectOptions['metadata']['hasBAMPFAmetadata'] in ("False",False):
			statusMessages[anObject]['Warnings'].append(
				"Note: we did not retrieve metadata from any BAMPFA "\
				"database (collection or audio)."
				)

	# except:
		# flash("There was an error with your request. Try again. :(")
	print(results)
	return render_template(
		'ingest/status.html',
		title='Ingest',
		statusMessages=statusMessages
		)
