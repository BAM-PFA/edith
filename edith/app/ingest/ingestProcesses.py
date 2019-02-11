#!/usr/bin/env python3
# standard library modules
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib

# non-standard modules
from flask_login import current_user

# local modules
from . import fmQuery
from . import dataSourceAccess
from .metadataMaster import metadataMasterDict
from .. import resourcespaceFunctions
from .. import sshStuff
from .. import utils

def get_acc_from_filename(basename):
	idRegex = re.compile(r'(.+\_)(\d{5})((\_.*)|($))')
	idMatch = re.match(idRegex, basename)
	if not idMatch == None: 
		idNumber = idMatch.group(2)
		if not idNumber == "00000":
			idNumber = idNumber.lstrip("0")
	else:
		idNumber = "--"	

	print("THIS IS THE ID NUMBER: "+idNumber)

	return idNumber

def get_barcode_from_filename(basename):
	barcodeRegex = re.compile(r"(.+\_\d{5}\_)(pm\d{7})(.+)",re.IGNORECASE)
	barcodeMatch = re.match(barcodeRegex,basename)
	if not barcodeMatch == None:
		barcode = barcodeMatch.group(2)
	else:
		barcode = "000000000"
	return barcode

def get_metadata(idNumber,basename,intermediateMetadata,dataSourceAccessDetails):
	# Init an empty dict for each item
	metadataDict = {}
	# Get the metadata master dict from metadataMaster.py
	# have to build up the metadataDict w each loop 
	# to avoid persisting metadata in subsequent loops
	for tag,mdValue in metadataMasterDict.items():
		metadataDict[tag] = mdValue

	# Add any existing field values to the blank dict
	if not intermediateMetadata == {}:
		for tag,mdValue in intermediateMetadata.items():
			if not mdValue == "":
				if tag in metadataDict:
					metadataDict[tag] = mdValue
	else:
		pass

	if all(value in ("",None) for value in metadataDict.values()):
		metadataDict['hasBAMPFAmetadata'] = False
	else:
		metadataDict['hasBAMPFAmetadata'] = True

	if idNumber == "--":
		print("NO PFA ID NUMBER")

	elif idNumber == '00000':
		# if the acc item number is zeroed out,
		# try looking for a barcode to search on
		try:
			barcode = get_barcode_from_filename(basename)
			# print(barcode)
			if barcode == "000000000":
				print("ID AND BARCODE BOTH ZEROED OUT")
				# return metadataDict

			else:
				FMmetadata = fmQuery.xml_query(barcode,dataSourceAccessDetails)
				if FMmetadata:
					# add any filemaker metadata to the dict
					for k,v in FMmetadata.items():
						if k in metadataDict:
							metadataDict[k] = v
					metadataDict['hasBAMPFAmetadata'] = True
		except:
			print("Error searching FileMaker on ID and barcode")
			# return metadataDict
	else:
		try:
			print('searching FileMaker on '+idNumber)
			FMmetadata = fmQuery.xml_query(idNumber,dataSourceAccessDetails)
			# print(FMmetadata)
			if FMmetadata:
				# add any filemaker metadata to the dict
				for k,v in FMmetadata.items():
					if k in metadataDict:
						metadataDict[k] = v
				metadataDict['hasBAMPFAmetadata'] = True
		except:
			# if no results, try padding with zeros
			idNumber = "{0:0>5}".format(idNumber)
			try:
				FMmetadata = fmQuery.xml_query(idNumber,dataSourceAccessDetails)
				# add any filemaker metadata to the dict
				if FMmetadata:
					for k,v in FMmetadata.items():
						if k in metadataDict:
							metadataDict[k] = v
					metadataDict['hasBAMPFAmetadata'] = True
			except:
				# give up
				pass

	# print('metadataDict')
	# print(metadataDict)
	return(metadataDict)

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
				# connection.sendCommand(command)
			except:
				print("Couldn't rsync the file...")

	else:
		print(
			"Your files are already on the current filesystem, "
			"so don't need to rsync anything."
			)

def write_metadata_json(metadata,basename):
	tempDir = utils.get_temp_dir()
	jsonPath = os.path.join(tempDir,basename+".json")
	# print(jsonPath)
	with open(jsonPath,'w+') as jsonTemp:
		json.dump(metadata,jsonTemp)#,ensure_ascii=False)
	# print(jsonPath)

	return jsonPath

def add_metadata(ingestDict):
	for objectPath, objectOptions in ingestDict.items():
		
		metadataSourceID = int(ingestDict[objectPath]['metadataSource'])
		if not metadataSourceID == 0:
			dataSourceAccessDetails = dataSourceAccess.main(metadataSourceID)
			
		metadataJson = {}
		metadataJson[objectPath] = {}
		# first check if there is user-supplied metadata
		if 'userMetadata' in ingestDict[objectPath]:
			metadataJson[objectPath]['metadata'] = \
				ingestDict[objectPath]['userMetadata']
		else:
			# if not, init an empty dict
			metadataJson[objectPath]['metadata'] = {}

		basename = objectOptions['basename']
		# try to parse an ID number
		idNumber = get_acc_from_filename(basename)
		intermediateMetadata = metadataJson[objectPath]['metadata']

		# go get some metadata
		metadata = get_metadata(idNumber,basename,intermediateMetadata,dataSourceAccessDetails)

		objectOptions['metadata'] = metadata

		metadataJson[objectPath]['metadata'] = metadata
		metadataJson[objectPath]['basename'] = basename
		objectOptions['metadataFilepath'] = \
			write_metadata_json(metadataJson,basename)

	# print(ingestDict)
	print("HELLO THERE WE ADDED METADATA!")
	# print(barf)
	return ingestDict

def make_pymm_command(user,_object,ingestDict):
	pythonBinary = utils.get_python_path()
	pymmPath = utils.get_pymm_path()
	ingestSipPath = os.path.join(pymmPath,'ingestSip.py')
	pymmCommand = [
		pythonBinary,	# path to python3 executable
		ingestSipPath,	# path to pymm folder
		'-i',_object,	# input path
		'-u',user,		# user gets recorded
		'-dz'			# report to db and delete originals
		]
	metadataFilepath = ingestDict[_object]['metadataFilepath']

	# IMPORTANT call to `777` the JSON file so pymm can read it
	os.chmod(metadataFilepath,0o777)
	if ingestDict[_object]['metadata']['hasBAMPFAmetadata'] != False:
		pymmCommand.extend(['-j',metadataFilepath])
	else:
		pass
	if 'concat reels' in ingestDict[_object].keys():
		if ingestDict[_object]['concat reels']:
			pymmCommand.extend(['-c'])

	return pymmCommand,metadataFilepath

def main(ingestDict):
	# TAKE IN A DICT OF {OBJECTS:OPTIONS/DETAILS}
	# run `pymm` on ingest objects
	# post access copies to resourcespace

	userFirstName = current_user.first_name
	userLastName = current_user.last_name
	# Construct the user's full name, unless the user is missing
	# one of these values (they shouldn't be...)
	if not any(x in (userFirstName,userLastName) for x in ("None",None)):
		user = "{} {}".format(userFirstName,userLastName)
	else:
		# otherwise default to the user's email address
		user = current_user.email

	# GET THE PYMM PATH TO CALL IN A SEC
	pymmPath = utils.get_pymm_path()
	ingestSipPath = os.path.join(pymmPath,'ingestSip.py')

	# get rid of the userMetadata dict if all the values are empty
	# it shouldn't be here but just in case....
	for _object,details in ingestDict.items():
		if 'userMetadata' in ingestDict[_object]:
			if all(value=="" for value in ingestDict[_object]['userMetadata'].values()):
				ingestDict[_object].pop('userMetadata')

	print("INGEST DICT LOOKS LIKE THIS NOW")
	for k,v in ingestDict.items():
		print(k)
		print(v)
		print("------")
	# get the hostname of the shared dir:
	_, hostName, _ = utils.get_shared_dir_stuff('shared')

	####################
	##### FETCH METADATA 
	####################
	ingestDict = add_metadata(ingestDict)

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
		for _object in ingestDict.keys():
			# ingestStatus is a set of messages that will be flashed to
			# the user. Compiling it as a list for now... seems simplest?
			ingestStatus = []

			# prep a pymm command
			pymmResult = None
			pymmCommand,metadataFilepath = make_pymm_command(user,_object,ingestDict)
			print(pymmCommand)

			try:
				pymmOut = subprocess.check_output(
					pymmCommand
					)
				# the last thing printed is the status dict....
				# get the pymm result dict via this highly hack-y method
				pymmOut = pymmOut.decode().split('\n')
				pymmResult = ast.literal_eval(pymmOut[-2])
				print(pymmResult)
				# get the UUID which we'll add to the metadata file in a sec
				ingestUUID = pymmResult['ingestUUID']

				ingestStatus.append(
					'Archival information package creation succeeeded'
					)
			except subprocess.CalledProcessError as e:
				print(e)
				ingestStatus.append(
					'Warning: Archival information package'\
					' creation failed'
					)

			try:
				with open(metadataFilepath,'r+') as mdread:
					print('opened the md file')
					data = json.load(mdread)
					key = list(data.keys())[0]
					data[key]['metadata']['ingestUUID'] = ingestUUID
					theGoods = data[key]['metadata']
				with open(metadataFilepath,'w+') as mdwrite:
					json.dump(theGoods,mdwrite)
					print('wrote to the md file')
				ingestStatus.append('Added metadata to sidecar JSON file')
			except:
				ingestStatus.append(
					'Warning: Problem writing to JSON metadata file.'\
					' Check file/folder permissions.'
					)
			########################
			#### RESOURCESPACE STUFF
			########################
			rsDir = utils.get_rs_dir()
			if pymmResult:
				rsProxyPath = pymmResult['accessPath']
				basename = ingestDict[_object]['basename']
				#print(rsProxyPath)
				#print(os.path.exists(rsProxyPath))
				if os.path.exists(rsProxyPath):
					print("WOOOT")
					# rsStatus is True/False result
					rsStatus = resourcespaceFunctions.do_resourcespace(
						# user,
						rsProxyPath,
						metadataFilepath
						)
					if rsStatus:
						ingestStatus.append(
							'Added proxy file(s) '\
							'and metadata to resourcespace'
							)
					else:
						ingestStatus.append(
							'Warning: Problem sending file or metadata '\
							'or both to ResourceSpace.'
							)
				else:
					print("PROXY FILE PATH PROBLEMO")
					ingestStatus.append(
						"Problem accessing the resourcespace proxy file."\
						"Maybe it didn't get created?"\
						"Maybe check folder permissions."
						)

			ingestDict[_object]['ingestStatus'] = ingestStatus

	utils.clean_temp_dir('ingest')
	return(ingestDict)
