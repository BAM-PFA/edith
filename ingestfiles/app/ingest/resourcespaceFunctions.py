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
# nonstandard libraries
import requests
# local modules
from . import ingestProcesses
from .. import utils

def do_resourcespace(user):
	resourcespaceProxyDir = utils.get_rs_dir()
	success = False
	for item in os.listdir(resourcespaceProxyDir):
		idNumber = ingestProcesses.get_acc_from_filename(item)
		metadata = ingestProcesses.get_metadata(idNumber,item)
		if os.path.isfile(item):
			itempath = os.path.abspath(item)
			quotedPath = urllib.parse.quote(itempath, safe='')
			result = resourcespace_API_call(
				user,
				metadata,
				quotedPath,
				itempath
				)
			if result:
				success = True
		elif os.path.isdir(item):
			# if input is a dir of files get the first item,
			# post it to RS as a 'primary' and add the rest
			# as related files
			items = os.listdir(item)
			items.sort()
			coolItems = [x for x in items if not x.startswith('.')]
			primaryItem = coolItems[0]
			primaryPath = os.path.abspath(primaryItem)
			quotedPath = urllib.parse.quote(
				os.path.abspath(primaryPath),
				safe=''
				)
			# post the first/primary to RS and get its record ID
			primaryRecord = resourcespace_API_call(
				user,
				metadata,
				quotedPath,
				primaryPath
				)
			if primaryRecord:
				coolItems.pop(0)
				for _file in coolItems:
					itempath = os.path.abspath(item)
					quotedPath = urllib.parse.quote(itempath, safe='')
					result = rs_alt_file_API_call(
						user,
						primaryRecord,
						quotedPath,
						itempath
						)
					if result:
						coolItems.pop(
							coolItems.index(_file)
						)
				if len(coolItems) == 0:
					success = True
	if success:
		return True

def format_RS_POST(RSquery,APIkey):
	rs_base_url = utils.get_rs_base_url()
	sign = hashlib.sha256(APIkey.encode()+RSquery.encode())
	signDigest = sign.hexdigest()
	completePOST = "{}/api/?{}&sign={}".format(
		rs_base_url,
		RSquery,
		signDigest
		)

def make_RS_API_call(completePOST):
	try:
		resp = requests.post(completePOST)
		print(resp.text)
	except ConnectionError as err:
		print("BAD RS POST")
		raise err

	httpStatus = resp.status_code
	if httpStatus == 200:
		return resp.status,resp.text
	else:
		return resp.status,None

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
	completePOST = format_RS_POST(RSquery,APIkey)

	status,text = make_RS_API_call(completePOST)
	if status == 200:
		utils.delete_it(filePath)
	return text

def rs_alt_file_API_call(user,primaryRecord,quotedPath,filePath):
	rsUser,APIkey = utils.get_rs_credentials(user)
	basename = os.path.basename(filePath)
	extension = utils.get_extension(basename)
	RSquery = (
		"user={0}"
		"&function=add_alternative_file"
		"&param1={1}"
		"&param2={2}"
		"&param3="
		"&param4={2}"
		"&param5={3}"
		"&param6=&param7="
		"&param8={4}".format(
			rsUser,
			primaryRecord,
			basename,
			extension,
			quotedPath
			)
		)
	completePOST = format_RS_POST(RSquery,APIkey)

	status,text = make_RS_API_call(completePOST)
	if status == 200:
		utils.delete_it(filePath)
	return text

