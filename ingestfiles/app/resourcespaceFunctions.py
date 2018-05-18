#!/usr/bin/env python3
# standard library modules
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
# nonstandard libraries
import requests
# local modules
from . import utils

def do_resourcespace(user,proxyPath,metadataFilepath=None):
	'''
	uh...
	'''
	# print(proxyPath)
	success = False
	if metadataFilepath != None:
		with open(metadataFilepath,'r+') as mf:
			metadata = json.load(mf)
			print(metadata)

	urlMetadata = metadata_for_rs(metadata)

	if os.path.isfile(proxyPath):
		print("the input object is a file")
		quotedPath = urllib.parse.quote(proxyPath, safe='')	
		result = resourcespace_API_call(
				user,
				urlMetadata,
				quotedPath,
				proxyPath
				)
	elif os.path.isdir(proxyPath):
		print("the input object is a directory")
		items = os.listdir(proxyPath)
		items.sort()
		coolItems = [os.path.join(proxyPath,x) for x in items if not x.startswith('.')]
		print(coolItems)
		primaryItem = coolItems[0]
		quotedPath = urllib.parse.quote(
			primaryItem,
			safe=''
			)
		print(quotedPath)
		# post the first/primary to RS and get its record ID
		primaryRecord = resourcespace_API_call(
			user,
			urlMetadata,
			quotedPath,
			primaryItem
			)
		print('primaryRecord')
		print(primaryRecord)
		if primaryRecord not in (None,''):
			coolItems.pop(0)
			print(coolItems)
			for _file in coolItems:
				quotedPath = urllib.parse.quote(_file, safe='')
				result = rs_alt_file_API_call(
					user,
					primaryRecord,
					quotedPath,
					_file
					)
				if result:
					coolItems.pop(
						coolItems.index(_file)
					)
			if len(coolItems) == 0:
				success = True
	return success

def format_RS_POST(RSquery,APIkey):
	rs_base_url = utils.get_rs_base_url()
	sign = hashlib.sha256(APIkey.encode()+RSquery.encode())
	signDigest = sign.hexdigest()
	completePOST = "{}/api/?{}&sign={}".format(
		rs_base_url,
		RSquery,
		signDigest
		)
	return completePOST

def make_RS_API_call(completePOST):
	try:
		resp = requests.post(completePOST)
		# print(resp.text)
	except ConnectionError as err:
		print("BAD RS POST")
		raise err

	httpStatus = resp.status_code
	if httpStatus == 200:
		return httpStatus,resp.text
	else:
		return httpStatus,None

def resourcespace_API_call(user,metadata,quotedPath,filePath):
	rsUser,APIkey = utils.get_rs_credentials(user)
	RSquery = (
		"user={}"
		"&function=create_resource"
		"&param1=3"
		"&param2=0"
		"&param3={}"
		"&param4=&param5=&param6="
		"&param7={}".format(rsUser,quotedPath,metadata)
		)
	# print(RSquery)
	completePOST = format_RS_POST(RSquery,APIkey)
	print(completePOST)
	httpStatus,RSrecordID = make_RS_API_call(completePOST)
	print(httpStatus)
	print(RSrecordID)
	if httpStatus == 200:
		utils.delete_it(filePath)
	return RSrecordID

def rs_alt_file_API_call(user,primaryRecord,quotedPath,filePath):
	rsUser,APIkey = utils.get_rs_credentials(user)
	basename = os.path.basename(filePath)
	extension = utils.get_extension(basename).strip('.')
	size = str(os.stat(filePath).st_size)
	RSquery = (
		"user={0}"
		"&function=add_alternative_file"
		"&param1={1}"
		"&param2={2}"
		"&param3={2}"
		"&param4={2}"
		"&param5={3}"
		"&param6={4}"
		"&param7=3"
		"&param8={5}".format(
			rsUser,
			primaryRecord,
			basename,
			extension,
			size,
			quotedPath
			)
		)
	print(RSquery)
	completePOST = format_RS_POST(RSquery,APIkey)
	print(completePOST)
	status,text = make_RS_API_call(completePOST)
	print(status)
	print(text)
	if not text == 'false':
		utils.delete_it(filePath)
	return text

def metadata_for_rs(metadataJSON):
	'''
	Map metadata to RS field IDs
	Return URL-encoded JSON per RS API reqs.
	'''

	rsMetaDict = {}

	rsMetaDict[8] = metadataJSON['title']
	rsMetaDict[84] = metadataJSON['altTitle']
	rsMetaDict[85] = metadataJSON['releaseYear']
	rsMetaDict[86] = metadataJSON['accPref']
	rsMetaDict[87] = metadataJSON['accDepos']
	rsMetaDict[88] = metadataJSON['accItem']
	rsMetaDict[89] = metadataJSON['accFull']
	rsMetaDict[90] = metadataJSON['projGrp']
	rsMetaDict[3] = metadataJSON['country']
	rsMetaDict[91] = metadataJSON['directorsNames']
	rsMetaDict[92] = metadataJSON['credits']
	rsMetaDict[93] = metadataJSON['generalNotes']
	rsMetaDict[94] = metadataJSON['conditionNote']
	rsMetaDict[98] = metadataJSON['Barcode']
	rsMetaDict[99] = metadataJSON['language']
	rsMetaDict[100] = metadataJSON['soundCharacteristics']
	rsMetaDict[101] = metadataJSON['color']
	rsMetaDict[102] = metadataJSON['runningTime']
	rsMetaDict[103] = metadataJSON['medium']
	rsMetaDict[104] = metadataJSON['dimensions']
	rsMetaDict[105] = metadataJSON['videoFormat']
	rsMetaDict[106] = metadataJSON['videoStandard']
	rsMetaDict[95] = metadataJSON['ingestUUID']
	# rsMetaDict[] = metadataJSON['']
	
	rsMetaJSON = json.dumps(rsMetaDict)
	quotedJSON = urllib.parse.quote(rsMetaJSON.encode())

	return quotedJSON
