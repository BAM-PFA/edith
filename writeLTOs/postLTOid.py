#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

from login import login
import os, subprocess, hashlib, json, paramiko, requests
import urllib.parse

# LTOid = sys.argv[1]

destination = "ltoer"
user = login(destination)[0]
cred = login(destination)[1]


def getRSid(resource):
	query = "user="+user+"&function=do_search&param1="+resource+"&param2=3&param3=title&param4=0&param5=1000&param6=desc"
	# print(query)
	sign = hashlib.sha256(cred.encode()+query.encode())
	signDigest = sign.hexdigest()
	completePOST = 'http://localhost/~RLAS_Admin/resourcespace/api/?'+query+"&sign="+signDigest
	# print(completePOST)
	try:
		resp = requests.post(completePOST)
		if not resp == "":
			ref = json.loads(resp.text)
			ref = dict(ref[0])
			ref = ref["ref"]
			return ref
		else:
			return "null"
	except Error as err:
		print("OOPS "*100)
		print(err)

def postLTOid(resource,tape):
	RSid = getRSid(resource)
	if not RSid == "null":
		query = "user="+user+"&function=update_field&param1="+RSid+"&param2=97&param3="+tape
		print(query)
		sign = hashlib.sha256(cred.encode()+query.encode())
		signDigest = sign.hexdigest()
		completePOST = 'http://localhost/~RLAS_Admin/resourcespace/api/?'+query+"&sign="+signDigest
		# print(completePOST)
		try:
			resp = requests.post(completePOST)
			print(resp)
			return resp
		except ConnectionError as err:
			print("OOPS "*100)
			print(err)
	else:
		return 0