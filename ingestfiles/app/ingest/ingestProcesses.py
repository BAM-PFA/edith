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

def get_acc_from_filename(basename):
	idRegex = re.compile(r'(.+\_)(\d{5})(\_.*)')
	idMatch = re.match(idRegex, basename)
	if not idMatch == None: 
		idNumber = idMatch.group(2)
		idNumber = idNumber.lstrip("0")
	else:
		idNumber = "0"	

	return idNumber

def ingestToResourceSpace(user,filePath, basename):
	idNumber = get_acc_from_filename(basename)
	
	targetFile = resourceTargetDir+basename
	quotedPath = urllib.parse.quote(targetFile, safe='')
	metadata = query(idNumber,filePath,basename)

	resourceSpaceAPIcall(user,metadata,quotedPath,targetFile)


def main(ingestDict):
	for objectPath, options in ingestDict.items():
		metadataDict = {}
		basename = options['basename']
		idNumber = get_acc_from_filename(basename)
		# print(idNumber)
		if idNumber != '0':
			metadataDict = fmQuery.xml_query(idNumber)
		else:
			metadataDict = {'title':basename}
		# print(metadataDict)
		options['metadata'] = metadataDict
		print(ingestDict)
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