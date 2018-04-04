#!/usr/bin/env python3
# standard library modules
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
from . import resourcespaceFunctions
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
	if idNumber == '--':
		metadataDict = {'title':'No metadata'}
	elif idNumber == '00000':
		# if the acc item number is zeroed out,
		# try looking for a barcode to search on
		try:
			barcode = get_barcode_from_filename(basename)
			# print(barcode)
			if barcode == "000000000":
				metadataDict = {'title':'No metadata'}
			else:
				metadataDict = fmQuery.xml_query(barcode)
		except:
			metadataDict = {'title':'No metadata'}
	else:
		try:
			print('searching on '+idNumber)
			metadataDict = fmQuery.xml_query(idNumber)
			# print('metadataDict')
		except:
			# if no results, try padding with zeros
			idNumber = "{0:0>5}".format(idNumber)
			try:
				metadataDict = fmQuery.xml_query(idNumber)
			except:
				# give up
				metadataDict = {'title':'No metadata'}
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
	# print(tempDir)
	jsonPath = os.path.join(tempDir,basename+".json")
	print(jsonPath)
	with open(jsonPath,'w+') as jsonTemp:
		json.dump(metadata,jsonTemp)

	return jsonPath

def main(ingestDict,user):
	# TAKE IN A DICT OF {OBJECTS:OPTIONS/DETAILS}
	# pymmconfig = pymmFunctions.read_config()
	# print(pymmconfig['paths']['outdir_ingestfile'])
	print(ingestDict)
	dirName, hostName, sourceDir = utils.get_shared_dir_stuff()

	# try to search filemaker for descriptive metadata
	for objectPath, options in ingestDict.items():
		metadataJson = {}
		metadataJson[objectPath] = {}
		basename = options['basename']
		idNumber = get_acc_from_filename(basename)
		metadata = get_metadata(idNumber,basename)
		options['metadata'] = metadata
		metadataJson[objectPath]['metadata'] = metadata
		metadataJson[objectPath]['basename'] = basename
		if metadata['title'] != 'No metadata':
			metadataFile = write_metadata_json(metadataJson,basename)
			# print(metadataFile)
		else:
			metadataFile = None

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
			if metadataFile:
				pymmCommand.extend(['-j',metadataFile])
			else:
				pass
			subprocess.call(pymmCommand)

	else:
		for _object in ingestDict.keys():
			pythonBinary = utils.get_python_path()
			pymmPath = utils.get_pymm_path()
			ingestSipPath = os.path.join(pymmPath,'ingestSip.py')
			pymmCommand = [pythonBinary,ingestSipPath,'-i',_object,'-u',user]
			if metadataFile:
				pymmCommand.extend(['-j',metadataFile])
			else:
				pass
			
			subprocess.call(pymmCommand)
			
			print('hey')

	resourcespaceFunctions.do_resourcespace(user)
	# print(ingestDict)
	return(ingestDict)
