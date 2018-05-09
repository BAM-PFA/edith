#!/usr/bin/env python3
# standard library modules
# import getpass
import ast
import json
from multiprocessing.dummy import Pool as ThreadPool
import os
import re
import subprocess
import sys
from time import sleep
import urllib
import uuid
# non-standard libraries
import wtforms
from flask import render_template, url_for, request, redirect, jsonify
from werkzeug import MultiDict
# local modules
from . import lto
from . import forms
from . import mountClass
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

		os.remove(tempFile)

	mountEmUp.tapeBarcodes.data = barcodes

	return render_template(
		'mount_lto.html',
		title="Mount LTO tapes",
		currentLTOid = utils.get_current_LTO_id(),
		mountForm=mountEmUp,
		barcodes=barcodes
		)


def run_ltfs(devname,tempdir,mountpoint):
	command = (
		"ltfs -f "
		"-o work_directory={} "
		"-o noatime "
		"-o capture_index "
		"-o devname={} "
		"{}".format(tempdir,devname,mountpoint)
		)
	commandList = command.split()
	print(commandList)
	doit = subprocess.Popen(
		commandList,
		stdin=subprocess.DEVNULL,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
		close_fds=True
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
	# this is dumb. the dict is passed as a string from the form
	# so i have to re-read it as a dict
	coolBarcodes = ast.literal_eval(coolBarcodes)
	devices = {'/dev/nst0':'','/dev/nst0':''}

	devices['/dev/nst0'] = coolBarcodes['A']
	devices['/dev/nst1'] = coolBarcodes['B']

	ltfsDetails = []

	for device, tapeID in devices.items():
		mountpoint = os.path.join(tempDir,tapeID)
		if os.path.exists(mountpoint):
			try:
				os.rmdir(mountpoint)
				os.mkdir(mountpoint,mode=0o777)
				print("made the mountpoint at {}".format(mountpoint))
			except:
				print("mountpoint dir exists and is not empty...")
		else:
			try:
				os.mkdir(mountpoint,mode=0o777)
				print("made the mountpoint at {}".format(mountpoint))
			except:
				print("can't make the mountpoint... check yr permissions")

		details = [device,tempdir,mountpoint]
		ltfsDetails.append(details)

	print(ltfsDetails)
	pool = ThreadPool(2)
	pool.starmap(run_ltfs,ltfsDetails)
	pool.close()
	# wait for the tapes to mount
	sleep(9)
	mountedDevices = []
	successes = []
	with subprocess.Popen(['mount'],stdout=subprocess.PIPE) as mount:
		for line in mount.stdout.read().splitlines():
			if '/dev/nst' in line:
				mountedDevices.append(line)
	for device, tapeID in devices.items():
		statuses[tapeID] = ''
		for item in mountedDevices:
			if device in item:
				statuses[tapeID] = 'mounted, ready to go'
			else:
				pass
		if not statuses[tapeID] == 'mounted, ready to go':
			statuses[tapeID] = 'not mounted, there was an error'


	return render_template(
		'mount_status.html',
		title="LTO Mount Status",
		statuses=statuses
		)
