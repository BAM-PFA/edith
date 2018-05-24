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
# local modules
from . import fmQuery
from . import metadataMaster
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



def get_metadata(idNumber,basename):
	# added in multiple return statements
	# somehow if there was no metadata the variable 
	# remembered the previous assignment and gave the current
	# file the same metadata. still have no idea how that happens.
	metadataDict = metadataMaster.metadata
	if idNumber == "--":
		print("NO EFFING ID NUMBER")
		for key, value in metadataDict.items():
			metadataDict[key] = ""

		metadataDict['hasBAMPFAmetadata'] = False

		return metadataDict

	elif idNumber == '00000':
		# if the acc item number is zeroed out,
		# try looking for a barcode to search on
		try:
			barcode = get_barcode_from_filename(basename)
			# print(barcode)
			if barcode == "000000000":
				for key, value in metadataDict.items():
					metadataDict[key] = ""
				metadataDict['hasBAMPFAmetadata'] = False

				return metadataDict

			else:
				metadataDict = fmQuery.xml_query(barcode)
		except:
			metadataDict['hasBAMPFAmetadata'] = False

			return metadataDict
	else:
		try:
			print('searching on '+idNumber)
			metadataDict = fmQuery.xml_query(idNumber)
			metadataDict['hasBAMPFAmetadata'] = True
			print('metadataDict')
		except:
			# if no results, try padding with zeros
			idNumber = "{0:0>5}".format(idNumber)
			try:
				metadataDict = fmQuery.xml_query(idNumber)
				metadataDict['hasBAMPFAmetadata'] = True
			except:
				# give up
				metadataDict['hasBAMPFAmetadata'] = False
				
				return metadataDict

	#print(metadataDict)
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
	# print(tempDir)
	jsonPath = os.path.join(tempDir,basename+".json")
	# print(jsonPath)
	with open(jsonPath,'w+') as jsonTemp:
		json.dump(metadata,jsonTemp)
	print(jsonPath)

	return jsonPath

def add_metadata(ingestDict):
	for objectPath, options in ingestDict.items():
		metadataJson = {}
		metadataJson[objectPath] = {}

		basename = options['basename']
		idNumber = get_acc_from_filename(basename)

		metadata = get_metadata(idNumber,basename)
		options['metadata'] = metadata

		metadataJson[objectPath]['metadata'] = metadata
		metadataJson[objectPath]['basename'] = basename

		options['metadataFilepath'] = write_metadata_json(metadataJson,basename)

	#print(ingestDict)
	print("HELLO THERE")
	return ingestDict

def main(ingestDict,user):
	# TAKE IN A DICT OF {OBJECTS:OPTIONS/DETAILS}
	# run `pymm` on ingest objects
	# post access copies to resourcespace
	print("INGEST DICT LOOKS LIKE THIS NOW")
	for k,v in ingestDict.items():
		print(k)
		print(v)
		print("------")
	dirName, hostName, sourceDir = utils.get_shared_dir_stuff('shared')
	# try to search filemaker for descriptive metadata
	ingestDict = add_metadata(ingestDict)
	#print(ingestDict)
	if not hostName == 'localhost':
		for objectPath in ingestDict.keys():
			try:
				grab_remote_files(objectPath)
			except:
				print("no dice.")
		for _object in os.listdir(utils.get_temp_dir()):
			objectPath = os.path.join(utils.get_temp_dir(),_object)
			pythonBinary = utils.get_python_path()
			pymmPath = utils.get_pymm_path()
			ingestSipPath = os.path.join(pymmPath,'ingestSip.py')
			pymmCommand = [pythonBinary,ingestSipPath,'-i',objectPath,'-u',user]
			metadataFilepath = ingestDict[_object]['metadataFilepath']
			if metadataFilepath != '':
				pymmCommand.extend(['-j',metadataFilepath])
			else:
				pass

			subprocess.call(pymmCommand)

	else:
		for _object in ingestDict.keys():
			pythonBinary = utils.get_python_path()
			pymmPath = utils.get_pymm_path()
			ingestSipPath = os.path.join(pymmPath,'ingestSip.py')
			pymmCommand = [pythonBinary,ingestSipPath,'-i',_object,'-u',user]
			metadataFilepath = ingestDict[_object]['metadataFilepath']
			#print(metadataFilepath)

			os.chmod(metadataFilepath,0o777)
			if ingestDict[_object]['metadata']['hasBAMPFAmetadata'] != False:
				pymmCommand.extend(['-j',metadataFilepath])
			else:
				pass
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

			except subprocess.CalledProcessError as e:
				print(e)

			print('hey')
			# add the UUID to the metadata file
			ingestUUID = pymmResult['ingestUUID']

			with open(metadataFilepath,'r+') as mdread:
				print('opened')
				data = json.load(mdread)
				key = list(data.keys())[0]
				data[key]['metadata']['ingestUUID'] = ingestUUID
				theGoods = data[key]['metadata']
				#print(theGoods)
			with open(metadataFilepath,'w+') as mdwrite:
				json.dump(theGoods,mdwrite)
			rsDir = utils.get_rs_dir()
			rsProxyPath = pymmResult['accessPath']
			basename = ingestDict[_object]['basename']
			#print(rsProxyPath)
			#print(os.path.exists(rsProxyPath))
			if os.path.exists(rsProxyPath):
				print("WOOOT")
				rsStatus = resourcespaceFunctions.do_resourcespace(
					user,
					rsProxyPath,
					metadataFilepath
					)

				#print(rsStatus)
			else:
				print("PATH PROBLEMO")
	return(ingestDict)
