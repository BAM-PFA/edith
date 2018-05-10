#!/usr/bin/env python3
# standard library modules
import ast
from multiprocessing.dummy import Pool as ThreadPool
import os
import re
import subprocess
import sys
from time import sleep
# non-standard libraries
from flask import render_template, request
import wtforms
# local modules
from . import forms
from . import lto
from . import ltoProcesses

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

# def run_ltfs(devname,tempdir,mountpoint):
# 	command = (
# 		"sudo ltfs "
# 		"-o gid=33 "
# 		"-o uid=33 "
# 		"-o work_directory={} "
# 		"-o noatime "
# 		"-o capture_index "
# 		"-o devname={} "
# 		"{}".format(tempdir,devname,mountpoint)
# 		)
# 	commandList = command.split()
# 	print(commandList)
# 	doit = subprocess.Popen(
# 		commandList,
# 		stdin=subprocess.DEVNULL,
# 		stdout=subprocess.DEVNULL,
# 		stderr=subprocess.PIPE,
# 		close_fds=True
# 		)
# 	for line in doit.stderr.read().splitlines():
# 		print(line.decode())


@lto.route('/mount_status',methods=['GET','POST'])
def mount_status():
	statuses = {'errors':[]}
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
				os.mkdir(mountpoint)
				os.chmod(mountpoint,0o777)
				print("made the mountpoint at {}".format(mountpoint))
			except:
				error = "mountpoint dir exists and is not empty..."
				statuses['errors'].append(error)
				print(error)
		else:
			try:
				os.mkdir(mountpoint)
				os.chmod(mountpoint,0o777)
				print("made the mountpoint at {}".format(mountpoint))
			except:
				error = "can't make the mountpoint... check yr permissions"
				statuses['errors'].append(error)
				print(error)

		details = [device,tempDir,mountpoint]
		ltfsDetails.append(details)

	print(ltfsDetails)
	pool = ThreadPool(2)
	pool.starmap(ltoProcesses.run_ltfs,ltfsDetails)
	pool.close()
	# wait for the tapes to mount
	sleep(13)
	mountedDevices = []
	successes = []
	with subprocess.Popen(['mount'],stdout=subprocess.PIPE) as mount:
		for line in mount.stdout.read().splitlines():
			if '/dev/nst' in line.decode():
				mountedDevices.append(line.decode())
	print(mountedDevices)
	for device, tapeID in devices.items():
		statuses[tapeID] = ''
		for item in mountedDevices:
			if tapeID in item:
				print("THIS TAPE YO")
				print(tapeID)
				statuses[tapeID] = 'mounted, ready to go'
			else:
				pass
		if not statuses[tapeID] == 'mounted, ready to go':
			statuses['errors'].append("error mounting{}".format(tapeID))
			statuses[tapeID] = 'not mounted, there was an error'


	return render_template(
		'mount_status.html',
		title="LTO Mount Status",
		statuses=statuses
		)

@lto.route('/list_aips',methods=['GET','POST'])
def list_aips():
	objects = listObjects.list_objects('aip')

	# need to get a human readable targetBase:
	# do a query (WHERE??) on the ingest UUID to retrieve the original filename
	# options:
	# the pymm database
	# resourcespace
	# drill into the AIP structure and look for the pbcore xml filename and parse that

	class one_aip(forms.aip_object_form):
		# http://wtforms.simplecodes.com/docs/1.0.1/specific_problems.html
		pass
	choices = {}
	for path,_object in objects.items():
		choices[path] = one_aip(targetPath=path,targetBase=_object)

	form = forms.write_to_LTO()
	form.suchChoices = choices

	return render_template(
		'list_aips.html',
		title="LTO write status",
		objects=objects,
		form=form
		)
@lto.route('/write_status',methods=['GET','POST'])
def write_status():
	_data = request.form.to_dict(flat=False)

	return render_template(
		'write_status.html',
		title="Write status",
		_data=_data
		)
	
