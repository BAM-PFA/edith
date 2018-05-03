#!/usr/bin/env python3
# standard library modules
import json
import os
import sys
import urllib
import uuid
# non-standard libraries
import wtforms
from flask import render_template, url_for, request, redirect, jsonify
from werkzeug import MultiDict
# local modules
from . import lto
from . import forms
from .. import listObjects
from .. import utils


@lto.route('/lto_menu',methods=['GET','POST'])
def lto_menu():

	return render_template(
		'lto_menu.html',
		title='LTO MENU'
		)


@lto.route('/format_lto',methods=['GET','POST'])
def format_lto():
	# we're going to store the current LTO id for the "A" tape in a text file.
	# get the value of that ID for processing/display/mounting LTO later.
	tmpDir = utils.get_temp_dir()
	ltoIdFilePath = os.path.join(tmpDir,'LTOID.txt')
	if not os.path.exists(ltoIdFilePath):
		with open(ltoIdFilePath,'w') as idfile:
			idfile.write('no lto id in use')
	with open(ltoIdFilePath,'r') as idfile:
		currentLTOid = idfile.readline().strip()

	newLTOid = forms.LTO_id_form()

	return render_template(
		'format_lto.html',
		title="Format LTO",
		IDform=newLTOid,
		currentLTOid=currentLTOid
		)

@lto.route('/lto_id',methods=['GET','POST'])
def lto_id():
	try:
		_data = request.form.to_dict(flat=False)
		ltoID = request.form['tapeAid']

