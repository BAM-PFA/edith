#!/usr/bin/env python3

import hashlib
import json
import os
import re
import requests
import subprocess
import sys
import time
import urllib

from . import fmQuery
from ..pymm import pymmFunctions

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

def ingestToResourceSpace(user,filePath, basename):
	idNumber = get_acc_from_filename(basename)
	
	targetFile = resourceTargetDir+basename
	quotedPath = urllib.parse.quote(targetFile, safe='')
	metadata = query(idNumber,filePath,basename)

	resourceSpaceAPIcall(user,metadata,quotedPath,targetFile)


def get_metadata(idNumber,basename):
	if idNumber == '--':
		metadataDict = {'title':basename}
	elif idNumber == '00000':
		# if the acc item number is zeroed out,
		# try looking for a barcode to search on
		try:
			barcode = get_barcode_from_filename(basename)
			# print(barcode)
			if barcode == "000000000":
				metadataDict = {'title':'THIS IS AN UNACCESSIONED PFA ITEM WITH NO BARCODE...'}
			else:
				metadataDict = fmQuery.xml_query(barcode)
		except:
			metadataDict = {'title':'THIS IS AN UNACCESSIONED PFA ITEM WITH NO FILEMAKER MATCH...'}
	else:
		try:
			metadataDict = fmQuery.xml_query(idNumber)
		except:
			# if no results, try padding with zeros
			idNumber = "{0:0>5}".format(idNumber)
			try:
				metadataDict = fmQuery.xml_query(idNumber)
			except:
				# give up
				metadataDict = {'title':basename}
	# print(metadataDict)
	return(metadataDict)


def main(ingestDict):
	# TAKE IN A DICT OF {OBJECTS:OPTIONS/DETAILS}
	pymmconfig = pymmFunctions.read_config()
	print(pymmconfig['paths']['outdir_ingestfile'])
	for objectPath, options in ingestDict.items():
		basename = options['basename']
		idNumber = get_acc_from_filename(basename)
		metadata = get_metadata(idNumber,basename)
		options['metadata'] = metadata

	# print(ingestDict)
	return(ingestDict)


### LEGACY STUFF: TO BE ADAPTED OR DELETED ###

# PROCESS INPUT FILES WITH mediamicroservices
# def do_legacy_mm():
# 	for item in os.listdir(mmIngestFolder):
# 		if not item.startswith("."):
# 			filePath = os.path.abspath(mmIngestFolder+"/"+item)
# 			fileNameForMediaID = os.path.splitext(item)[0]
# 			try:
# 				ingest = subprocess.Popen(['/usr/local/bin/ingestfile','-e','-u',user,'-I',filePath,'-m',fileNameForMediaID])
# 				ingest.wait()
# 				os.remove(filePath)
# 			except IOError as err:
# 				print("OS error: {0}".format(err))

# # SEND AIP THAT HAS BEEN CREATED TO THE LTO STAGING AREA
# def do_legacy_AIP(LTOstageDir):
# 	for AIP in os.listdir(LTOstageDir):
# 		dirPath = LTOstageDir+AIP
# 		if os.path.isdir(dirPath):
# 			if "bagit.txt" not in os.listdir(dirPath):
# 				print(AIP+" is an AIP! Let's Bag It!")
# 				try:
# 					subprocess.call([bagit,"--contact-name",user,dirPath])
# 				except:
# 					print("OS error: {0}".format(err))
# 			else:
# 				print(AIP+" was arlready bagged!")

# # INGEST THE PROXY FILE AND METADATA INTO RESOURCESPACE
# def do_legacy_rs(resourceTargetDir):
# 	for basename in os.listdir(resourceTargetDir):
# 		filePath = resourceTargetDir+basename
# 		user = user
# 		if os.path.isfile(filePath):
# 			if not basename.startswith("."):
# 				ingestToResourceSpace(user,filePath,basename)

# def do_legacy_resourceSpaceAPIcall(user,metadata,filePath,RSfile):
# 	# print(user)
# 	destination = user
# 	user = login(destination)[0]
# 	cred = login(destination)[1]

# 	RSquery = "user="+user+"&function=create_resource_from_local&param1=3&param2=0&param3="+filePath+"&param4=&param5=&param6=&param7="+metadata
# 	sign = hashlib.sha256(cred.encode()+RSquery.encode())
# 	signDigest = sign.hexdigest()
# 	completePOST = 'http://localhost/~RLAS_Admin/resourcespace/api/?'+RSquery+"&sign="+signDigest
	
# 	try:
# 		resp = requests.post(completePOST)
# 		print(resp.text)
# 	except ConnectionError as err:
# 		print("OOPS "*100)
# 		raise err

# 	print(resp.status_code)
# 	httpStatus = resp.status_code
# 	if httpStatus == 200:
# 			os.remove(RSfile)
