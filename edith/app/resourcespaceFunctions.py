#!/usr/bin/env python3
# standard library modules
import codecs
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
# nonstandard libraries
from flask_login import current_user
import requests
# local modules
from . import utils

def do_resourcespace(proxyPath,metadataFilepath=None):
	'''
	take in the object(s) and process them according to file/dir status
	'''
	# print(proxyPath)
	success = False
	if metadataFilepath != None:
		with open(metadataFilepath,'r+') as mf:
			metadata = json.load(mf)
			print("READING JSON IN THE RS PROCESS")
			print(metadata)

			# HOW TF DOES THIS HANDLE NO METADATA? don't remember.... :(
	else:
		mdDict = '{"frameRateProxy":""}'
		metadata= json.loads(mdDict)
	# urlMetadata = metadata_for_rs(metadata)

	if os.path.isfile(proxyPath):
		print("the input object is a file")
		frameRateProxy = utils.get_proxy_framerate(proxyPath)
		metadata['frameRateProxy'] = frameRateProxy
		urlMetadata = metadata_for_rs(metadata)
		quotedPath = urllib.parse.quote(proxyPath, safe='')	
		result = resourcespace_API_call(
				urlMetadata,
				quotedPath,
				proxyPath
				)
		if result not in (None,'','Invalid signature'):
			success = True

	elif os.path.isdir(proxyPath):
		print("the input object is a directory")
		items = os.listdir(proxyPath)
		items.sort()
		coolItems = [os.path.join(proxyPath,x) for x in items if not x.startswith('.')]
		print(coolItems)
		primaryItem = coolItems[0]
		# RS only has metadata per primary item, so hopefully all the reels have
		# the same framerate.
		frameRateProxy = utils.get_proxy_framerate(primaryItem)
		metadata['frameRateProxy'] = frameRateProxy
		urlMetadata = metadata_for_rs(metadata)
		quotedPath = urllib.parse.quote(
			primaryItem,
			safe=''
			)
		# print(quotedPath)
		# post the first/primary to RS and get its record ID
		primaryRecord = resourcespace_API_call(
			urlMetadata,
			quotedPath,
			primaryItem
			)
		print('primaryRecord')
		print(primaryRecord)
		if primaryRecord not in (None,'','Invalid signature'):
			coolItems.remove(primaryItem)
			# print(coolItems)
			while len(coolItems) > 0:
				alt = coolItems[0]
				print("I want to post {} as an alt file!!".format(alt))
				# print(coolItems)
				quotedPath = urllib.parse.quote(alt, safe='')
				result = rs_alt_file_API_call(
					primaryRecord,
					quotedPath,
					alt
					)
				print("RESULT: {}".format(result))
				if result not in (None, False, 'false','','Invalid signature'):
					coolItems.remove(
						alt
					)
				else:
					break
			if len(coolItems) == 0:
				success = True
		else:
			pass
	return success

def format_RS_POST(RSquery,APIkey):
	'''
	Take in the base query,
	add the RS URL,
	sign it w API key,
	return completePOST
	'''

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
	'''
	This actually does the POST.
	Made via requests.post()
	'''
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

def resourcespace_API_call(metadata,quotedPath,filePath):
	'''
	make a call to the RS create_resource() function
	'''
	rsUser = current_user.RSusername
	APIkey = current_user.RSkey
	RSquery = (
		"user={}"
		"&function=create_resource"
		"&param1=14"
		"&param2=0"
		"&param3={}"
		"&param4=&param5=&param6="
		"&param7={}".format(
			rsUser,
			quotedPath,
			metadata
			)
		)
	# print(RSquery)
	completePOST = format_RS_POST(RSquery,APIkey)
	print(completePOST)
	httpStatus,RSrecordID = make_RS_API_call(completePOST)
	print(httpStatus)
	print("hey")
	print(RSrecordID)
	if httpStatus in ('200',200) and not "Invalid signature" in RSrecordID:
		print("SUCCESS! POSTED THE THING TO RS")
		utils.delete_it(filePath)
	return RSrecordID

def rs_alt_file_API_call(primaryRecord,quotedPath,filePath):
	'''
	post any alternative files to the rs record for the primary object
	'''
	rsUser = current_user.RSusername
	APIkey = current_user.RSkey
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
	# print(RSquery)
	completePOST = format_RS_POST(RSquery,APIkey)
	print(completePOST)
	status,text = make_RS_API_call(completePOST)
	# print(status)
	# print(text)
	if not text == 'false':
		utils.delete_it(filePath)
	return text

def metadata_for_rs(metadataJSON):
	'''
	Map metadata to RS field IDs
	Return URL-encoded JSON per RS API reqs.
	'''

	rsMetaDict = {}

	rsMetaDict[1] = metadataJSON['tags']
	rsMetaDict[3] = metadataJSON['country']
	rsMetaDict[8] = metadataJSON['title']
	rsMetaDict[29] = metadataJSON['nameSubjects']
	rsMetaDict[76] = metadataJSON['frameRateProxy']
	rsMetaDict[84] = metadataJSON['altTitle']
	rsMetaDict[85] = metadataJSON['releaseYear']
	rsMetaDict[86] = metadataJSON['accPref']
	rsMetaDict[87] = metadataJSON['accDepos']
	rsMetaDict[88] = metadataJSON['accItem']
	rsMetaDict[89] = metadataJSON['accFull']
	rsMetaDict[90] = metadataJSON['projGrp']
	rsMetaDict[91] = metadataJSON['directorsNames']
	rsMetaDict[92] = metadataJSON['credits']
	rsMetaDict[93] = metadataJSON['generalNotes']
	rsMetaDict[94] = metadataJSON['conditionNote']
	rsMetaDict[95] = metadataJSON['ingestUUID']
	rsMetaDict[98] = metadataJSON['Barcode']
	rsMetaDict[99] = metadataJSON['language']
	rsMetaDict[100] = metadataJSON['soundCharacteristics']
	rsMetaDict[101] = metadataJSON['color']
	rsMetaDict[102] = metadataJSON['runningTime']
	rsMetaDict[103] = metadataJSON['medium']
	rsMetaDict[104] = metadataJSON['dimensions']
	rsMetaDict[105] = metadataJSON['videoFormat']
	rsMetaDict[106] = metadataJSON['videoStandard']
	rsMetaDict[107] = metadataJSON['eventTitle']
	rsMetaDict[108] = metadataJSON['eventYear']
	rsMetaDict[109] = metadataJSON['eventFullDate']
	rsMetaDict[110] = metadataJSON['eventSeries']
	rsMetaDict[111] = metadataJSON['eventRelatedExhibition']
	rsMetaDict[112] = metadataJSON['eventLocation']
	rsMetaDict[113] = metadataJSON['description']
	rsMetaDict[114] = metadataJSON['creator']
	rsMetaDict[115] = metadataJSON['creatorRole']
	rsMetaDict[116] = metadataJSON['eventOrganizer']
	rsMetaDict[117] = metadataJSON['assetExternalSource']
	rsMetaDict[118] = metadataJSON['copyrightStatement']
	rsMetaDict[119] = metadataJSON['restrictionsOnUse']
	rsMetaDict[120] = metadataJSON['generation']
	rsMetaDict[121] = metadataJSON['frameRateTRTdetails']
	rsMetaDict[122] = metadataJSON['platformOutlet']
	rsMetaDict[123] = metadataJSON['editSequenceSettings']
	rsMetaDict[124] = metadataJSON['additionalCredits']
	rsMetaDict[125] = metadataJSON['postProcessing']
	rsMetaDict[126] = metadataJSON['exportPublishDate']
	rsMetaDict[127] = metadataJSON['PFAfilmSeries']
	rsMetaDict[128] = metadataJSON['recordingDate']
	rsMetaDict[129] = metadataJSON['digitizedBornDigital']
	rsMetaDict[130] = metadataJSON['digitizer']
	rsMetaDict[131] = metadataJSON['locationOfRecording']
	rsMetaDict[132] = metadataJSON['speakerInterviewee']
	rsMetaDict[133] = metadataJSON['filmTitleSubjects']
	rsMetaDict[134] = metadataJSON['topicalSubjects']
	# rsMetaDict[] = metadataJSON['']
	
	rsMetaJSON = json.dumps(rsMetaDict,ensure_ascii=False)
	# print(rsMetaJSON)
	quotedJSON = urllib.parse.quote(rsMetaJSON.encode())
	if "%5Cn" in quotedJSON:
		print("REPLACING NEWLINES")
		quotedJSON = quotedJSON.replace('%5Cn','%3Cbr%2F%3E')

	return quotedJSON

def getRSid(AIP):
	'''
	Search for a resource record by its ingest UUID
	'''
	rsUser = current_user.RSusername
	APIkey = current_user.RSkey
	RSquery = (
		"user={}"
		"&function=do_search"
		"&param1={}"
		"&param2="
		"&param3=title"
		"&param4=0"
		"&param5=10"
		"&param6=desc".format(
			rsUser,
			AIP
			)
		)
	# print(query)
	completePOST = format_RS_POST(RSquery,APIkey)
	print(completePOST)
	status,text = make_RS_API_call(completePOST)
	try:
		# RS should return a JSON object of the search results
		searchResult = json.loads(text)
		print(searchResult)
		searchJSON = dict(searchResult[0])
		RSid = searchJSON["ref"]
	except:
		print("No resourcespace record returned")
		RSid = None

	print(RSid)
	return RSid

def post_LTO_id(AIP,ltoID):
	'''
	Search RS for the record pertaining to the AIP object.
	Post the LTO id to the record.
	'''
	postStatus = False
	rsUser = current_user.RSusername
	APIkey = current_user.RSkey
	RSid = getRSid(AIP)
	if RSid:
		RSquery = (
			"user={}"
			"&function=update_field"
			"&param1={}"
			"&param2=96"
			"&param3={}".format(
				rsUser,
				RSid,
				ltoID
				)
			)

		completePOST = format_RS_POST(RSquery,APIkey)
		status,text = make_RS_API_call(completePOST)

		if text in (True,"True","true"):
			postStatus = True
		else:
			print("Couldn't post the LTO ID to resourcespace")

	else:
		print("Trouble searching RS for the AIP unique ID ({}).".format(AIP))

	return postStatus

