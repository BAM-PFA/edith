#!/usr/bin/env python3
# standard library modules
import ast
from datetime import datetime
import json
from multiprocessing import Pool
import os
import re
import subprocess
# import sys
# from time import sleep
# non-standard libraries
# from flask import render_template, request
# import wtforms
# local modules
from .. import resourcespaceFunctions
from .. import utils

from .. import db
from .. models import Tape, TapeID

# class LTODeck():
# 	"""Instance of the deck during an LTO interaction... WIP"""
# 	def __init__(self):
# 		self.a_drive_device = "/dev/nst0"
# 		self.b_drive_device = "/dev/nst1"

# 	def set_tape_IDs(self,aTapeID=None,bTapeID=None):
# 		pass

class Package():
	"""docstring for Package"""
	def __init__(self, 
		path=None,
		size=None
		):
		
		self.path = path
		self.size = size
		
class FreshTape():
	"""Class to define an LTO tape"""
	def __init__(self,
		device=None,
		tapeID=None,
		UUID=None,
		noTape=None,
		dbID=None,
		unformatted=None,
		mountpoint=None,
		spaceAvailable=None
		):
		self.device = device 			# e.g., "/dev/nst0"
		self.tapeID = tapeID 			# 6-digit barcode "19091A"
		self.UUID = UUID				# 32-byte UUID
		self.noTape = noTape 			# true if the drive is just empty
		self.unformatted = unformatted	# true if there's a new blank tape
		self.mountpoint = mountpoint 	# mountpoint in temp directory
		self.spaceAvailable = spaceAvailable

		self.formatStatus = None
		self.mountStatus = None

	def format_me(self):
		MKLTFS = [
			'mkltfs',#'-f',
			'--device={}'.format(self.device),
			'--tape-serial={}'.format(self.tapeID),
			'--volume-name={}'.format(self.tapeID)
			]

		try:
			out, err = subprocess.Popen(
				MKLTFS,
				stdout=subprocess.PIPE
				).communicate()
			# print(out)

			# FROM LTFS SPEC: 
			# **LTFS15047E error = Medium is already formatted**
			# "The format operation failed because the medium is already formatted by LTFS."
			

			if not "LTFS15047E" in err.decode():
				self.formatStatus = "Formatted as LTFS"
				for line in err.splitlines():
					if "Volume UUID" in line.decode():
						self.UUID = line.decode().strip().split()[5]
			else:
				# this shouldn't even be needed @ this point....
				self.formatStatus = "The format operation failed because the medium is already formatted by LTFS."

		except:
			self.formatStatus = "there was an error in the LTFS command execution... needs manual investigation?"

	def insert_me(self):
		# make a db record for the tape
		newTape = Tape(
			tapeBarcode=self.tapeID,
			tapeUUID=self.UUID,
			status="unmounted",
			# formattedDate=datetime.now(),
			spaceAvailable=self.spaceAvailable
			)

		try:
			db.session.add(newTape)
		except Exception as e:
			print(e)
		db.session.commit()
		self.dbID = newTape.id

	def mount_me(self):
		pass

	def write_status_to_db(self):
		pass
		
class WriteProcess():
	"""docstring for WriteProcess"""
	def __init__(self,
		arg=None
		):
		self.arg = arg
		
class TapeMount():
	"""docstring for TapeMount"""
	def __init__(self, 
		mountpoint=None
		):
		self.mountpoint = mountpoint
		

def get_aip_human_name(aipPath):
	'''
	ALERT: THIS IS A HACK!!!
	Peer into the UUID named AIP and find the PBCore XML file for the asset,
	which *should* be named after the canonical name of the ingested object.
	Then return this human-readable name so that it can be listed for writing
	to LTO. 
	It is 100 percent possible/likely that this is a dumb way of finding
	what we are looking for, but it's a quick&dirty solution that should also
	mostly work.
	'''
	# init humanName as False in preparation for failure
	humanName = False
	if os.path.exists(aipPath):
		# going to assume that the AIP follows the current structure for this
		# so there is a parent dir named after the ingest UUID
		# and under that there is a metadata dir and in that is the pbcore 
		# xml file that contains the human-readable name that we want
		UUID = os.path.basename(aipPath)
		metadataDir = os.path.join(aipPath,UUID,'metadata')
		if os.path.exists(metadataDir):
			for thing in os.listdir(metadataDir):
				# REDO THIS WITH GLOB
				if "_pbcore.xml" in thing:
					# GRAB THE HUMAN NAME
					humanName = thing.replace("_pbcore.xml","")
				else:
					pass
		else:
			print("there is no metadata dir in the AIP??")

	else:
		print(
			"the aip path you provided ({}) does not exist.".format(aipPath)
			)

	return humanName

def run_ltfs(devname,tempdir,mountpoint):
	command = (
		"sudo ltfs "
		"-o gid=33 "
		"-o uid=33 "
		"-o work_directory={} "
		"-o noatime "
		"-o capture_index "
		"-o devname={} "
		"{}".format(tempdir,devname,mountpoint)
		)
	commandList = command.split()
	# print(commandList)
	doit = subprocess.Popen(
		commandList,
		stdin=subprocess.DEVNULL,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.PIPE,
		close_fds=True
		)
	for line in doit.stderr.read().splitlines():
		print(line.decode())

	return doit.stderr

def run_moveNcopy(aipPath,tapeMountpoint):
	pythonBinary = utils.get_python_path()
	pymmPath = utils.get_pymm_path()
	moveNcopyPath = os.path.join(pymmPath,'moveNcopy.py')
	command = (
		"{} {} "
		"-s "
		"-i {} "
		"-d {}".format(
			pythonBinary,
			moveNcopyPath,
			aipPath,
			tapeMountpoint
			)
		)

	commandList = command.split()
	print(commandList)
	runit = subprocess.run(
		commandList,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
		)
	for line in runit.stdout.splitlines():
		print(line.decode())
	for line in runit.stderr.splitlines():
		print(line.decode())

	return runit.stdout


def write_LTO(aipDict):
	aMount,bMount = get_tape_mountpoints()
	print(aMount,bMount)
	sipWriteTuples = []
	if not False in (aMount,bMount):
		for tapeMountpoint in (aMount,bMount):
			for path,stuff in aipDict.items():
				# get aip paths and tape mountponts 
				# to build commands for both tapes
				details = [path,tapeMountpoint]
				sipWriteTuples.append(details)
	else:
		status = ("Couldn't read the tape stats file "
			"or it doesn't exist. Try remounting the tapes or check "
			"the tapes manually. Or check file permissions on edith/app/tmp?"
			)

		return (False,status)

	# print(sipWriteTuples)
	# this is a mutli-*process* call instead of a multithread call, 
	# which reduces the back and forth on LTO (apparently)
	try:
		pool = Pool(2)
		poolresult = pool.starmap(run_moveNcopy,sipWriteTuples)
		pool.close()
		print(poolresult)
		return (poolresult,"")
	except:
		return (False,"Error in the write process...")

def read_LTO(pathList):
	'''
	pathList should contain the full path to each selected AIP
	on the mounted tape
	'''
	_, _, dip_out = utils.get_shared_dir_stuff('dip')
	dipWriteTuples = []
	for AIP in pathList:
		inOut = [AIP,dip_out]
		dipWriteTuples.append(inOut)

	print(dipWriteTuples)
	try:
		pool = Pool(2)
		poolresult = pool.starmap(run_moveNcopy,dipWriteTuples)
		pool.close()
		print(poolresult)
		return poolresult
	except:
		return False


def write_LTO_temp_stats():
	'''
	Save the stats on mounted tapes to a temp file for reading
	by various processes.
	This file gets deleted on unmounting tapes (after writes?)
	'''

	stats = {
		"A":{
			"mountpoint":"",
			"spaceAvailable":""
			},
		"B":{
			"mountpoint":"",
			"spaceAvailable":""
			}
		}
	dfProcess = subprocess.run(['df'],stdout=subprocess.PIPE)
	dfTape = [
		line.decode() for line in dfProcess.stdout.splitlines() 
		if '/dev/nst' in line.decode()
		]
	for line in dfTape:
		if '/dev/nst0' in line:
			stats["A"]["mountpoint"] = line.split()[5]
			stats["A"]["spaceAvailable"] = line.split()[3]
		elif '/dev/nst1' in line:
			stats["B"]["mountpoint"] = line.split()[5]
			stats["B"]["spaceAvailable"] = line.split()[3]

	tempDir = utils.get_temp_dir()
	statsJsonPath = os.path.join(tempDir,"tempTapeStats.json")
	print(stats)
	try:
		with open(statsJsonPath,"x") as f:
			pass
		os.chmod(statsJsonPath,0o777)
		with open(statsJsonPath,"w") as f:
			json.dump(stats,f)
		return True
	except:
		print("couldn't write the temp tape stats file")
		return False

def get_tape_contents(deck):
	contents = {'status':False}
	if 'A' in deck:
		theDeck = "A"
	elif 'B' in deck:
		theDeck = "B"
	aMount,bMount = get_tape_mountpoints()
	if not False in (aMount,bMount):
		if theDeck == "A":
			contents = list_aips_on_tape(aMount,contents)
		elif theDeck == 'B':
			contents = list_aips_on_tape(bMount,contents)
	else:
		contents = ("Couldn't read the tape stats file "
			"or it doesn't exist. Try remounting the tapes or check "
			"the tapes manually. Or check file permissions on edith/app/tmp?"
			)

	return contents

def list_aips_on_tape(mountpoint,contents):
	if mountpoint == False:
			contents['status'] = False
	else:
		contents['status'] = True
		for item in os.listdir(mountpoint):
			aipPath = os.path.join(mountpoint,item)
			humanName = get_aip_human_name(aipPath)
			aipSize = utils.get_object_size(aipPath)
			aipHumanSize = utils.humansize(aipSize)
			contents[aipPath]= {}
			contents[aipPath]['humanName'] = humanName
			contents[aipPath]['aipSize'] = aipSize
			contents[aipPath]['aipHumanSize'] = aipHumanSize

	return contents


def get_tape_stats():
	tempDir = utils.get_temp_dir()
	statsJsonPath = os.path.join(tempDir,"tempTapeStats.json")
	try:
		with open(statsJsonPath,'r') as f:
			stats = json.load(f)
	except:
		try:
			with open(statsJsonPath,'r') as f:
				stats = f.read()
				stats = ast.literal_eval(stats)
		except:
			print("couldn't read the stats file or it doesn't exist")
			stats = "couldn't read the stats file or it doesn't exist"

	return stats

def get_tape_mountpoints():
	stats = get_tape_stats()
	if not stats == "couldn't read the stats file or it doesn't exist":
		aMount = stats["A"]["mountpoint"]
		bMount = stats["B"]["mountpoint"]
	else:
		aMount = bMount = False

	return aMount,bMount

def unmount_tapes():
	# apache user added to sudoers overrides for `umount`
	aMount,bMount = get_tape_mountpoints()
	errors = []
	if not False in (aMount,bMount):
		for tape in (aMount,bMount):
			command = [
			'sudo','umount',
			tape
			]
			out = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			if not out.stderr.decode() == '':
				errors.append(out.stderr.decode())
			else:
				pass
	if not errors == []:
		return errors
	else:
		return True

def parse_index_schema_file():
	# get the first and last name of current_user
	user = utils.construct_user_name()
	print("PARSING LTFS SCHEMA FILE")
	pythonBinary = utils.get_python_path()
	pymmPath = utils.get_pymm_path()
	ltfsSchemaParserPath = os.path.join(pymmPath,'ltfsSchemaParser.py')
	aTapeID = get_current_LTO_id()
	tempDir = utils.get_temp_dir()
	aTapeSchema = os.path.join(tempDir,aTapeID+".schema")
	parseCommand = [
		pythonBinary,
		ltfsSchemaParserPath,
		'-l',aTapeSchema,
		'-u',user
		]

	if os.path.isfile(aTapeSchema):
		out = subprocess.run(
			parseCommand,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
			)
		print(out.stdout)

	else:
		print("SCHEMA FILE DOESN'T EXIST?")

def establish_new_lto_id(ltoID):
	ltoIDregex = re.compile(r'^((\d{4}[A-Z]A)|(\d{5}A))$')
	# ltoIdFilePath = os.path.join(utils.get_temp_dir(),'LTOID.txt')
	error = None
	try:
		db.session.query(TapeID).delete() # clear out any lingering entries
		db.session.commit()
	except:
		pass 

	if re.match(tapeIdRegex,ltoID):
		aVersion = ltoID
		bVersion = ltoID[:-1]+"B"
		try:
			newID = TapeID(id=1, a_version=aVersion, b_version=bVersion)
			db.session.add(newID)
			db.session.commit()
			ltoIDstatus = True
		except:
			error = 'There was an error adding the LTO ID to the database.'
			ltoIDstatus = False

	return error, ltoIDstatus

def get_current_LTO_id():
	try:
		currentLTOid = db.session.query(TapeID).get(1).a_version
	except:
		currentLTOid = None

	return currentLTOid

def get_a_and_b_IDs():
	# Read the current LTO ID from db
	# and return the ID for both A and B tapes
	currentLTOid = db.session.query(TapeID).get(1)
	if currentLTOid:
		aTapeID = currentLTOid.a_version
		bTapeID = currentLTOid.b_version
	else:
		aTapeID = None
		bTapeID = None

	return aTapeID,bTapeID

# def search_for_existing_tape(aTapeID,bTapeID):
# 	aTape = db.session.query(Tape).filter(tapeBarcode=aTapeID).first()
# 	bTape = db.session.query(Tape).filter(tapeBarcode=bTapeID).first()

# 	return aTape, bTape

def prep_tapes(aTapeID,bTapeID):
	aTape = get_tape_details(aTapeID,"/dev/nst0")
	bTape = get_tape_details(bTapeID,"/dev/nst1")

	return aTape,bTape

def get_tape_details(tapeID,device):
	# this check should happen after the db has been 
	# searched for any previous tapes with the ID
	command = ['ltfs','-f','-o','devname={}'.format(device)]
	name = None
	spaceAvailable = 0
	unformatted = False
	noTape = False
	error = False
	tapeID = tapeID
	try:
		# purposefully fail to mount device,
		# parse stderr, and get the tape details from it
		# returns a FreshTape object w these details
		out,err = subprocess.Popen(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
			).communicate()
		
		for line in err.splitlines():
			if "Volume Name" in line.decode():
				name = line.decode().strip().split()[5]
			elif "Volser(Barcode)" in line.decode():
				tapeID = line.decode().strip().split()[4]
			elif "Volume UUID" in line.decode():
				UUID = line.decode().strip().split()[5]
			elif "LTFS17168E" in line.decode():
				# "Cannot read volume: medium is not partitioned"
				# i.e. the tape is not formatted w LTFS
				unformatted = True 
			elif "LTFS11006E" in line.decode():
				# "Cannot read volume: failed to load the tape"
				# taking this to mean that there's no tape in the drive
				# (or perhaps the tape is unreadable 
				# and functionally the drive is empty)
				noTape = True
			elif "LTFS10030I" in line.decode():
				try:
					spaceAvailable = int(line.decode().strip().split()[20])
					spaceAvailable = utils.mebibytes_to_bytes(spaceAvailable)
				except:
					pass

		if name and unformatted and "null" not in name:
			tape = FreshTape(
				device=device,
				tapeID=tapeID,
				spaceAvailable=spaceAvailable,
				unformatted=unformatted,
				noTape=noTape,
				error=error
				)

	except:
		error = "Unable to get details about {} drive... try turning it off and on again".format(device)
		tape = FreshTape(error=error,tapeID=tapeID)

	return tape
	
def post_tape_id_to_rs(writeStatuses):
	stats = get_tape_stats()
	ltoID = os.path.basename(stats["A"]["mountpoint"])
	for AIP, status in writeStatuses.items():
		if "True" in status:
			resourcespaceFunctions.post_LTO_id(AIP,ltoID)
