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
from . import metadataQuery
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
	CurrentIngest = ingestProcesses.IngestProcess()
	CurrentIngest.status = 'form submitted ok'
	print(CurrentIngest.status)
	# CurrentIngest.user = CurrentIngest.get_user(CurrentIngest)
	print(CurrentIngest.user)
	
	_data = request.form.to_dict(flat=False)
	print(_data)
	# sys.exit
	CurrentIngest = ingestProcesses.parse_raw_ingest_form(_data,CurrentIngest)
	# sys.exit
	# pass dict of files:options to ingestProcesses.main() and get back
	# a dict that includes metadata
	CurrentIngest = ingestProcesses.main(CurrentIngest)

	return render_template(
		'ingest/status.html',
		title='Ingest',
		CurrentIngest=CurrentIngest
		)
