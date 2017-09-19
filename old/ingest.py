#!/usr/bin/env python3

# import requests
import json, hashlib, os, os.path, re, urllib, subprocess, time
import sys

from fmQuery.py import query
from login import login

authorized_users = ['shibata@berkeley.edu','davetaylor@berkeley.edu','gibbscman@berkeley.edu','mcq@berkeley.edu']
mmIngestFolder = '/Users/RLAS_Admin/Sites/ingest/uploads'
resourceTargetDir = "/Users/RLAS_Admin/Sites/resourceTarget/"

# inputFile = sys.argv[1]
user = sys.argv[1]

def resourceSpaceAPIcall(metadata,filePath):
	destination = "resourcespace"
	user = login(destination)[0]
	cred = login(destination)[1]

	query = "user="+user+"&function=create_resource_from_local&param1=3&param2=0&param3="+filePath+"&param4=&param5=&param6=&param7="+metadata
	sign = hashlib.sha256(cred.encode()+query.encode())
	signDigest = sign.hexdigest()
	
	# destination = "red"
	# user = login(destination)[0] 
	# cred = login(destination)[1]

	# completePOST = 'http://'+user+':'+cred+'@10.253.22.21:/~'+user+'/resourcespace/api/?'+query+"&sign="+signDigest
	completePOST = 'http://localhost/RLAS_Admin/resourcespace/api/?'+query+"&sign="+signDigest
	# print(completePOST)
	
	try:
		resp = requests.post(completePOST)
		# print(resp.text)
	except ConnectionError as err:
		print("OOPS "*25)
		raise err

	print(resp.status_code)

def ingestToResourceSpace(resource, basename):
	print(resource)
	idRegex = re.compile(r'(.+\_)(\d{5})(\_.*)')
	idMatch = re.match(idRegex, basename)
	idNumber = idMatch.group(2)
	# print(idNumber)	
	
	targetDir = "/Users/RLAS_Admin/Sites/resourceTarget/"
	targetFile = targetDir+basename
	quotedPath = urllib.parse.quote(targetFile, safe='')

	################################
	# TEST METADATA SINCE FM ISNT AVAILABLE NOW
	metadata = {  
      "84":"mysummary",
      "8":"mytitle",
	   }
	jasoned = json.dumps(metadata)
	quotedJasoned = urllib.parse.quote(jasoned.encode())
	resourceSpaceAPIcall(quotedJasoned,quotedPath)
	#
	####################

	# resourceSpaceAPIcall(query(idNumber,basename),quotedPath)

for item in os.listdir(mmIngestFolder):
	print(item)
	if not item.startswith("."):
		filePath = os.path.abspath(mmIngestFolder+"/"+item)
		fileNameForMediaID = os.path.splitext(item)[0]
		try:
			subprocess.call(['/usr/local/bin/ingestfile','-e','-u',user,'-I',filePath,'-m',fileNameForMediaID])
		except IOError as err:
			print("OS error: {0}".format(err))

for resource in os.listdir(resourceTargetDir):
	filePath = resourceTargetDir+resource
	if os.path.isfile(filePath):
		if not resource.startswith("."):
			ingestToResourceSpace(filePath,resource)