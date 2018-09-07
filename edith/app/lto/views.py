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

	if statuses['errors'] == []:
		# if there were no errors, write the current tapes stats
		# to a temp file for later reading/processing
		tempStats = ltoProcesses.write_LTO_temp_stats()
		if tempStats:
			statuses['errors'] = 'No errors. :)'

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
		humanName = ltoProcesses.get_aip_human_name(path)
		aipSize = ltoProcesses.aip_size(path)
		# convert aip size from bytes to human readable form
		aipHumanSize = utils.humansize(aipSize)
		if not humanName == False:
			choices[path] = one_aip(
				targetPath=path,
				targetBase=humanName,
				aipSize=aipSize,
				aipHumanSize=aipHumanSize
				)
		else:
			choices[path] = one_aip(
				targetPath=path,
				targetBase=_object,
				aipSize=aipSize,
				aipHumanSize=aipHumanSize
				)

	form = forms.write_to_LTO()
	form.suchChoices = choices

	spaceAvailable = ltoProcesses.get_tape_stats()
	if not spaceAvailable == "NO STATS AVAILABLE":
		for tape, stats in spaceAvailable.items():
			# the `df` command that gets space available
			# defaults to 1024-byte blocks
			oneKiBblocks = stats['spaceAvailable']
			bytes = int(oneKiBblocks)*1024
			space = utils.humansize(bytes)
			stats['spaceAvailableHuman'] = space

	else:
		spaceAvailable = {}
		spaceAvailable["NONE"] = {"spaceAvailableHuman":"NO TAPES FOUND, BUDDY!!"}

	return render_template(
		'list_aips.html',
		title="List AIPs available",
		objects=objects,
		spaceAvailable=spaceAvailable,
		form=form
		)

@lto.route('/write_status',methods=['GET','POST'])
def write_status():
	# raw data from the form
	_data = request.form.to_dict(flat=False)
	# print(_data)
	user = request.form['user']

	results = {}
	toWrite = []
	targetPaths = {}
	aipSizes = []
	for key,value in _data.items():
		if 'writeToLTO' in key:
			toWrite.append(key.replace('writeToLTO-',''))
		elif 'targetPath' in key:
			# make a dict entry for {objectName:aipPath}
			targetPaths[key.replace('targetPath-','')] = value[0]
		elif 'aipSize' in key:
			aipSizes.append(value[0])
	for _object in toWrite:
		# build a dict of AIPS to write
		for objectName,aipPath in targetPaths.items():
			if objectName == _object:
				results[aipPath] = {'canonicalName' : objectName}

	# print(results)
	writeStatuses = {}
	writeResults = ltoProcesses.write_LTO(results,user)
	print("LTO WRITE RESULTS:")
	print(writeResults)
	for result in writeResults:
		#print(result)
		resultString = str(result)
		#print(resultString)
		if "HASHDEEP" in resultString:
			sip = result.decode().split('|')[1]
			#print(sip)
			aipStatus =  result.decode().split('|')[2].rstrip()
			#print(aipStatus)
			writeStatuses[sip] = aipStatus
	print(writeStatuses)

	# remove staged AIPs ~~THIS DOESN'T EXIST YET!~~
	# ltoProcesses.remove_staged_AIPs(writeStatuses)
	
	ltoProcesses.post_tape_id_to_rs(writeStatuses,user)
	ltoProcesses.unmount_tapes()
	utils.clean_temp_dir()
	# PARSE THE UPDATED SCHEMA FILE
	ltoProcesses.parse_index_schema_file(user)


	return render_template(
		'write_status.html',
		title="Write status",
		writeResults=writeStatuses,
		_data=_data
		)
