#!/usr/bin/env python3
# standard library modules
import json
import os
import re
import subprocess
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


# we're going to store the current LTO id for the "A" tape in a text file.
# get the value of that ID for processing/display/mounting LTO later.


@lto.route('/lto_menu',methods=['GET','POST'])
def lto_menu():

	return render_template(
		'lto_menu.html',
		title='LTO MENU'
		)


@lto.route('/format_lto',methods=['GET','POST'])
def format_lto():
	currentLTOid = utils.get_current_LTO_id()

	newLTOid = forms.LTO_id_form()
	formatLTO = forms.format_form()

	return render_template(
		'format_lto.html',
		title="Format LTO",
		IDform=newLTOid,
		formatForm=formatLTO,
		currentLTOid=currentLTOid
		)

@lto.route('/lto_id',methods=['GET','POST'])
def lto_id():
	tapeIdRegex = re.compile(r'^((\d{4}[A-Z]A)|(\d{5}A))$')
	ltoIDstatus = False
	try:
		_data = request.form.to_dict(flat=False)
		ltoID = request.form['tapeAid']
		if re.match(tapeIdRegex,ltoID):
			with open(ltoIdFilePath,'w') as idfile:
				idfile.write(ltoID)
			ltoIDstatus = True
		else:
			ltoIDstatus = False
	except:
		_data = 'none'
		ltoID = 'none'

	return render_template(
		'lto_id.html',
		ltoID=ltoID,
		ltoIDstatus = ltoIDstatus
		)

@lto.route('/format_status',methods=['GET','POST'])
def format_status():
	# we are using SCSI (SAS) attached drives in linux so I'll defalt the 
	# device names to nst0 and nst1, which are the non-auto-rewind device 
	# names
	aTapeID = utils.get_current_LTO_id()
	bTapeID = aTapeID[:-1]+"B"
	linuxDevices = {
		'/dev/nst0':aTapeID,
		'/dev/nst1':bTapeID
		}

	statuses = {
		"/dev/nst0":False
		"/dev/nst1":False
	}

	for device,tapeID in linuxDevices.items():
		MKLTFS = [
		'mkltfs',
		'--device={}'.format(device),
		'--tape-serial={}'.format(tapeID),
		'--volume-name={}'.format(tapeID)
		]

		try:
			out, err = subprocess.Popen(
				MKLTFS,
				stdout=subprocess.PIPE
				).communicate()
			statuses[device] = True

		except:
			statuses[device] = "can't format tape, maybe it's already formatted"


	return render_template(
		'format_status.html',
		statuses=statuses
		)




