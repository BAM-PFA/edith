#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

import requests
import json, hashlib, os, os.path, re, urllib.parse, subprocess, time

from login import login
from fmQuery import query

authorized_users = ['shibata@berkeley.edu','davetaylor@berkeley.edu','gibbscman@berkeley.edu','mcq@berkeley.edu']
mmIngestFolder = '/Users/RLAS_Admin/Sites/ingest/uploads/'
resourceTargetDir = "/Users/RLAS_Admin/Documents/Video-Ingests/mmOutDir/resourcespace_output/"
LTOstageDir = "/Volumes/maxxraid1/LTO_STAGE/"
bagit = "/Library/Frameworks/Python.framework/Versions/3.6/bin/bagit.py"

user = sys.argv[1]
print(user)

def resourceSpaceAPIcall(user,metadata,filePath,RSfile):
	print(user)
	destination = user
	user = login(destination)[0]
	cred = login(destination)[1]
	# print("^"*100+"\n\n\n\n"+user+"\n\n\n\n"+"^"*100)

	query = "user="+user+"&function=create_resource_from_local&param1=3&param2=0&param3="+filePath+"&param4=&param5=&param6=&param7="+metadata
	# print(query)
	sign = hashlib.sha256(cred.encode()+query.encode())
	signDigest = sign.hexdigest()
	completePOST = 'http://localhost/~RLAS_Admin/resourcespace/api/?'+query+"&sign="+signDigest
	# print(completePOST)
	
	try:
		resp = requests.post(completePOST)
		print(resp.text)
	except ConnectionError as err:
		print("OOPS "*100)
		raise err

	print(resp.status_code)
	httpStatus = resp.status_code
	if httpStatus == 200:
			os.remove(RSfile)

def ingestToResourceSpace(user,resource, basename):
	idRegex = re.compile(r'(.+\_)(\d{5})(\_.*)')
	idMatch = re.match(idRegex, basename)
	if not idMatch == None: 
		idNumber = idMatch.group(2)
	else:
		idNumber = "0"
	
	targetFile = resourceTargetDir+basename
	# print(targetFile)
	quotedPath = urllib.parse.quote(targetFile, safe='')
	metadata = query(idNumber,basename)
	# print(metadata)

	resourceSpaceAPIcall(user,metadata,quotedPath,targetFile)

for item in os.listdir(mmIngestFolder):
	# print(item)
	if not item.startswith("."):
		filePath = os.path.abspath(mmIngestFolder+"/"+item)
		fileNameForMediaID = os.path.splitext(item)[0]
		try:
			subprocess.call(['/usr/local/bin/ingestfile','-e','-u',user,'-I',filePath,'-m',fileNameForMediaID])
		except IOError as err:
			print("OS error: {0}".format(err))
		os.remove(filePath)

for AIP in os.listdir(LTOstageDir):
	dirPath = LTOstageDir+AIP
	if os.path.isdir(dirPath):
		if "bagit.txt" not in os.listdir(dirPath):
			print(AIP+" is an AIP! Let's Bag It!")
			try:
				subprocess.call([bagit,"--contact-name",user,dirPath])
			except:
				print("OS error: {0}".format(err))
		else:
			print(AIP+" was arlready bagged!")

for resource in os.listdir(resourceTargetDir):
	filePath = resourceTargetDir+resource
	user = user
	if os.path.isfile(filePath):
		if not resource.startswith("."):
			# print("@"*100+"\n\n\nINGESTING "+resource+" TO RESOURCESPACE\n\n\n"+"@"*100)
			ingestToResourceSpace(user,filePath,resource)