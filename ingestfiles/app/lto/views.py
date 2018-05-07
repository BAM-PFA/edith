#!/usr/bin/env python3
# standard library modules
# import getpass
import ast
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

@lto.route('/lto_menu',methods=['GET','POST'])
def lto_menu():
	return render_template(
		'lto_menu.html',
		title='LTO MENU'
		)


@lto.route('/format_lto',methods=['GET','POST'])
def format_lto():
	currentLTOid = utils.get_current_LTO_id()

	formatLTO = forms.format_form()

	return render_template(
		'format_lto.html',
		title="Format LTO",
		formatForm=formatLTO,
		currentLTOid=currentLTOid
		)

@lto.route('/format_status',methods=['GET','POST'])
def format_status():
	# we are using SCSI (SAS) attached drives in linux so I'll defalt the 
	# device names to nst0 and nst1, which are the non-auto-rewind device 
	# names
	linuxDevices = utils.get_devices()
	aTapeID, bTapeID = utils.get_a_and_b()
	linuxDevices["/dev/nst0"] = aTapeID
	linuxDevices["/dev/nst1"] = bTapeID

	statuses = {
		"/dev/nst0":False,
		"/dev/nst1":False
	}

	if not aTapeID == "no id" and not bTapeID == "no id":
		for device,tapeID in linuxDevices.items():
			# -f force option is here for testing ONLY @fixme remove it for production!
			MKLTFS = [
			'mkltfs','-f',
			'--device={}'.format(device),
			'--tape-serial={}'.format(tapeID),
			'--volume-name={}'.format(tapeID)
			]

			try:
				out, err = subprocess.Popen(
					MKLTFS,
					stdout=subprocess.PIPE
					).communicate()
				# statuses[device] = True
				print(out)
				if not "LTFS15047E" in out:
					statuses[device] = True
				else:
					statuses[device] = "can't format tape, maybe it's already formatted"

			except:
				statuses[device] = "there was an error in the LTFS command execution... meh?"
	else:
		for device,tapeID in linuxDevices.items():
			statuses[device] = "There doesn't appear to be a valid ID in place for the A and/or B tapes."

	return render_template(
		'format_status.html',
		statuses=statuses
		)

@lto.route('/lto_id',methods=['GET','POST'])
def lto_id():
	newLTOid = forms.LTO_id_form()
	currentLTOid = utils.get_current_LTO_id()
	return render_template(
		'lto_id.html',
		title='Create LTO ID',
		IDform=newLTOid,
		currentLTOid=currentLTOid
		)

@lto.route('/lto_id_status',methods=['GET','POST'])
def lto_id_status():
	tapeIdRegex = re.compile(r'^((\d{4}[A-Z]A)|(\d{5}A))$')
	ltoIDstatus = False
	ltoIdFilePath = os.path.join(utils.get_temp_dir(),'LTOID.txt')
	try:
		_data = request.form.to_dict(flat=False)
		ltoID = request.form['tapeAid']
		ltoIdFilePath = os.path.join(utils.get_temp_dir(),'LTOID.txt')
		if re.match(tapeIdRegex,ltoID):
			with open(ltoIdFilePath,'w') as idfile:
				idfile.write(ltoID)
			ltoIDstatus = True
		else:
			ltoIDstatus = False
	except:
		_data = 'there was an error'
		ltoID = 'there was an error'

	return render_template(
		'lto_id_status.html',
		ltoID=ltoID,
		title="LTO ID status",
		ltoIDstatus = ltoIDstatus
		)

@lto.route('/mount_lto',methods=['GET','POST'])
def mount_lto():

	mountEmUp = forms.mount()

	# get the current attached tape devices and try to read a barcode from each
	tempDir = utils.get_temp_dir()
	barcodes = {"A":"/dev/nst0","B":"/dev/nst1"}
	for letter, device in barcodes.items():
		# purposefully fail to mount each device,
		# send stderr to a text file to parse ,
		# and get the tape barcode from it
		now = utils.now()
		tempFile = os.path.join(tempDir,"{}_{}_temp.txt".format(letter,now))
		command = ['ltfs','-f','-o','devname={}'.format(device)]
		out,err = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
		#print(out)
		#print("that was out")
		#print(err)
		#print("that was err")
		with open(tempFile,'x') as x:
			pass
		with open(tempFile,'w+') as f:
			print("GETTING BARCODE FOR TAPE,HANG ON")
			for line in err.splitlines():
				print(line)
				f.write(line.decode())
				f.write('\n')
		if os.path.exists(tempFile):
			with open(tempFile,'r') as f:
				for line in f.readlines():
					if "Volser(Barcode)" in line:
						barcodeLine = line.strip().split()
						barcode = barcodeLine[4]
						print(barcode)
						barcodes[letter] = barcode
		else:
			barcodes[letter] = "Trouble getting the tape barcode"
		print(barcodes)

	mountEmUp.tapeBarcodes.data = barcodes

	return render_template(
		'mount_lto.html',
		title="Mount LTO tapes",
		currentLTOid = utils.get_current_LTO_id(),
		mountForm=mountEmUp,
		barcodes=barcodes
		)


@lto.route('/mount_status',methods=['GET','POST'])
def mount_status():
	statuses = {}
	userId = os.getegid()
	tempDir = utils.get_temp_dir()
	_data = request.form.to_dict(flat=False)
	print(_data)
	coolBarcodes = _data["tapeBarcodes"][0]
	print("barcodes")
	print(coolBarcodes)
	coolBarcodes = ast.literal_eval(coolBarcodes)
	print(type(coolBarcodes))
	devices = {'/dev/nst0':'','/dev/nst0':''}
	print(type(devices))

	devices['/dev/nst0'] = coolBarcodes['A']
	devices['/dev/nst1'] = coolBarcodes['B']

	for device, tapeID in devices.items():
		mountpoint = os.path.join(tempDir,tapeID)
		if os.path.exists(mountpoint):
			try:
				os.rmdir(mountpoint)
			except:
				print("mountpoint dir exists and is not empty...")
		else:
			try:
				os.mkdir(mountpoint,mode=0o777)
				#subprocess.call(['mkdir','-m','777',mountpoint])
			except:
				print("can't make the mount point... check yr permissions")
		# -o uid sets user to www-data (apache user)
		# -o umask sets permissions to 777
		LTFS = [
		'ltfs','-f',
		'-o','work_directory={}'.format(tempDir),
		'-o','noatime',
		'-o','capture_index',
		'-o','devname={}'.format(device),
		'-o','gid=33',
		'-o','umask=777',
		mountpoint
		]
		# print(LTFS)
		try:
			# subprocess.run(LTFS,stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
			# subprocess.run(LTFS,stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
			# pass the ltfs command as a list to a helper function
			# to try to get it to not block
			utils.mount_tape(LTFS)

			statuses[tapeID] = 'mounted, ready to go'
			print("I DID A SUBPROCESS LTFS...")
		except:
			statuses[tapeID] = 'there was an error in the LTFS command'

	return render_template(
		'mount_status.html',
		title="LTO Mount Status",
		statuses=statuses
		)
