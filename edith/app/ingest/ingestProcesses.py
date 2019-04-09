#!/usr/bin/env python3
# standard library modules
import ast
import json
import os
import re
import subprocess
import sys
import uuid

# non-standard modules
from flask_login import current_user

# local modules
from . import dataSourceAccess
from . import metadataMaster
from ..pymm import ingestSip
from .. import resourcespaceFunctions
from .. import sshStuff
from .. import utils

class IngestProcess:
	def __init__(self):
		self.user = self.get_user()
		self._uuid = str(uuid.uuid4())
		self.status = None

		# this is a list of objects being ingested
		self.Ingestibles = []

	def get_user(self):
		userFirstName = current_user.first_name
		userLastName = current_user.last_name
		# Construct the user's full name, unless the user is missing
		# one of these values (they shouldn't be...)
		if not any(x in (userFirstName,userLastName) for x in ("None",None)):
			user = "{} {}".format(userFirstName,userLastName)
		else:
			# otherwise default to the user's email address
			user = current_user.email

		print(user)
		return user

class Ingestible:
	'''
	This is a single object selected by a user to be ingested.
	'''
	def __init__(self, inputPath):
		self.inputPath = inputPath
		self.metadata = metadataMaster.Metadata(self.inputPath)

		self.doProres = None
		self.deliverMezzanine = None
		self.concatReels = None

		self.pymmArgv = []
		self.pymmResult = None
		self.accessCopyPath = None

		self.ingestWarnings = []
		self.ingestMessages = []

		self.status = None

def grab_remote_files(targetFilepath):
	# prep credentials to grab stuff from remote shared dir
	hostName, sourceDir, remoteAddress, remoteUser, remotePassword, sshKeyfile = utils.get_remote_credentials()
	processingDir = utils.get_temp_dir()
	print(processingDir)
	# double check that it's not on the current filesystem
	if not os.path.isfile(targetFilepath):
		if not os.path.isdir(targetFilepath):
			try:
				subprocess.call([
				'rsync','-rtvPihe','ssh',
				'{0}@{1}:{2}'.format(remoteUser,remoteAddress,targetFilepath),
				processingDir
				])
			except:
				print("Couldn't rsync the file...")

	else:
		print(
			"Your files are already on the current filesystem, "
			"so don't need to rsync anything."
			)

def add_metadata(CurrentIngest):
	for _object in CurrentIngest.Ingestibles:
		metadataSourceID = int(_object.metadata.metadataSource)
		if not metadataSourceID == 0:
			dataSourceAccessDetails = dataSourceAccess.main(metadataSourceID)
		else:
			dataSourceAccessDetails = None

		# go get some metadata
		_object.metadata.fetch_metadata(dataSourceAccessDetails)

		if _object.metadata.retrievedExternalMetadata == True:
			print("HELLO THERE WE ADDED METADATA!")
		else:
			_object.ingestWarnings.append(
				"Note: we did not retrieve metadata from any BAMPFA "\
				"database."
				)

		_object.metadata.set_hasBAMPFAmetadata()
		_object.metadata.clear_empty_metadata_fields()
		if _object.metadata.innerMetadataDict['hasBAMPFAmetadata'] == True:
			_object.metadata.write_json_file()

	return CurrentIngest

def set_pymm_sys_args(CurrentIngest,_object):

	_object.pymmArgv = [
	'',
	'-i',_object.inputPath,	# input path
	'-u',CurrentIngest.user,# user gets recorded
	'-dz'					# report to db and delete originals
	]
	metadataJSONpath = _object.metadata.metadataJSONpath
	# IMPORTANT call to `777` the JSON file so pymm can read it
	if os.path.isfile(metadataJSONpath):
		os.chmod(metadataJSONpath,0o777)
		_object.pymmArgv.extend(['-j',metadataJSONpath])

	if _object.concatReels:
		_object.pymmArgv.extend(['-c'])

def parse_raw_ingest_form(formData,CurrentIngest):
	'''
	Logic to parse the raw form data from ingest.views.status
	'''
	results = {}
	toIngest =[]
	targetPaths = []
	doProresYES = []
	proresToDaveYES = []
	doConcatYES =[]
	metadataSourceSelection = {}
	metadataEntries = {}

	for key, value in formData.items():
		# get names/paths of files we actually want to process
		if 'runIngest' in key:
			toIngest.append(key.replace('runIngest-',''))
		# targetPath is the path of the item coming from the form
		# I think targetPath includes *all the things* from the list, 
		# not just selected ones
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
				# see if its been added, if not make a new temp dict
				metadataEntries[theObject] = {}
				# `value` here is returned as a list 
				# from the metadata FormField
				metadataEntries[theObject][field] = value[0]
			else:
				metadataEntries[theObject][field] = value[0]

	for _object in toIngest:
		# build a dict of files:options
		for _path in targetPaths:
			if _object == os.path.basename(_path):
				ingestMe = Ingestible(_path)
				if _object in metadataEntries:
					# this line actually adds the user metadata to the 
					# object that's selected
					ingestMe.metadata.add_more_metadata(
						metadataEntries[_object]
						)
					print(ingestMe.metadata.innerMetadataDict)
				if _object in metadataSourceSelection:
					ingestMe.metadata.metadataSource = \
						metadataSourceSelection[_object]
				CurrentIngest.Ingestibles.append(ingestMe)


	# add boolean options to dict
	for ingestible in CurrentIngest.Ingestibles:
		if ingestible.metadata.basename in doProresYES:
			ingestible.doProres = True
		if ingestible.metadata.basename in proresToDaveYES:
			ingestible.deliverMezzanine = True
		if ingestible.metadata.basename in doConcatYES:
			ingestible.concatReels = True

	return CurrentIngest

def main(CurrentIngest):
	# TAKE IN AN `INGEST` OBJECT
	#   IT SHOULD CONTAIN AT LEAST ONE `INGESTIBLE`
	# run `pymm` on Ingestibles
	# post access copies to resourcespace

	# GET THE PYMM PATH TO CALL IN A SEC
	pymmPath = utils.get_pymm_path()
	ingestSipPath = os.path.join(pymmPath,'ingestSip.py')

	print("INGEST LOOKS LIKE THIS NOW")
	for item in CurrentIngest.Ingestibles:
		print(item.inputPath)
		print(item.metadata.metadataDict)
		print("------")
	# get the hostname of the shared dir:
	_, hostName, _ = utils.get_shared_dir_stuff('shared')

	####################
	##### FETCH METADATA 
	####################
	CurrentIngest = add_metadata(CurrentIngest)

	##############
	#### CALL PYMM
	##############
	if not hostName == 'localhost':
		'''
		THIS SECTION IS DEAD... WOULD NEED TO BE REVISED
		IF IT EVER SEEMED LIKE WE WANT TO MESS WITH REMOTE SHARED DIR
		for objectPath in ingestDict.keys():
			try:
				grab_remote_files(objectPath)
			except:
				print("no dice.")
		'''
	else:
		for _object in CurrentIngest.Ingestibles:
			metadataJSONpath = _object.metadata.metadataJSONpath

			set_pymm_sys_args(CurrentIngest,_object)

			try:
				sys.argv = _object.pymmArgv
				try:
					pymmIngest = ingestSip.main()
				except:
					break

				_object.pymmIngest = pymmIngest
				_object.pymmResult = pymmIngest.ingestResults
				# print("PYMM OUTPUT\n",_object.pymmResult)
				# sys.exit()

				# now work on metadata
				if not _object.pymmResult['status'] == False:
					_object.ingestMessages.append(
						'Archival information package'\
						' creation succeeeded'
						)
					# get the UUID which we'll add to the metadata file in a sec
					ingestUUID = _object.pymmResult['ingestUUID']
					try:
						with open(metadataJSONpath,'r+') as mdread:
							print('opened the md file')
							data = json.load(mdread)
							key = list(data.keys())[0]
							data[key]['metadata']['ingestUUID'] = ingestUUID
							theGoods = data[key]['metadata']
							print(theGoods)
							# also update the Ingestible attributes
							_object.metadata.innerMetadataDict = theGoods
							_object.metadata.metadataDict[_object.inputPath]\
								['metadata'] = theGoods

						with open(metadataJSONpath,'w+') as mdwrite:
							json.dump(theGoods,mdwrite)
							print('wrote to the md file')
						_object.ingestMessages.append(
							'Added metadata to sidecar JSON file: {}'.format(
								metadataJSONpath
								)
							)
					except:
						_object.ingestWarnings.append(
							'Warning: Problem writing to JSON metadata file:'\
							' {}.\nCheck file/folder permissions.'.format(
								metadataJSONpath
								)
							)
				else:
					_object.ingestWarnings.append(
						"Warning: "+str(_object.pymmResult['abortReason'])
						)

			except subprocess.CalledProcessError as e:
				print(e)
				_object.ingestWarnings.append(
					'Warning: Archival information package'\
					' creation failed'
					)

			print(_object.ingestWarnings,_object.ingestMessages)

			########################
			#### RESOURCESPACE STUFF
			########################
			rsDir = utils.get_rs_dir()
			if _object.pymmResult != None:
				if _object.pymmResult['status'] != False:

					_object.accessCopyPath = pymmIngest.accessDelivery

					basename = _object.metadata.basename

					if os.path.exists(_object.accessCopyPath):
						print("WOOOT")
						# rsStatus is True/False result
						rsStatus = resourcespaceFunctions.do_resourcespace(
							_object
							)
						if rsStatus:
							_object.ingestMessages.append(
								'Added proxy file(s) '\
								'and metadata to resourcespace'
								)
						else:
							_object.ingestWarnings.append(
								'Warning: Problem sending file or metadata '\
								'or both to ResourceSpace.'
								)
					else:
						print("PROXY FILE PATH PROBLEMO")
						_object.ingestWarnings.append(
							"Warning: Problem accessing the resourcespace proxy file."\
							"Maybe it didn't get created?"\
							"Maybe check folder permissions."
							)
			else:
				pass

			_object.metadata.delete_temp_JSON_file()

	return(CurrentIngest)
