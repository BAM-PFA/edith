#!/usr/bin/env python3
'''
This function queries defined external metadata source(s)
and builds out a dict of fields and values that maps to Bampfa
ResourceSpace and PBCore mappings.
'''
# standard libraries
import hashlib
import json
import os
import re
import requests
import subprocess
import sys
import urllib.parse
# non standard modules
from lxml import etree
# local imports
from . import metadataMaster
from config import app_config

def xml_query(idNumber,dataSourceAccessDetails):
	metadataMappings = app_config['METADATA_MAPPINGS']

	dsn = dataSourceAccessDetails['dataSourceName']
	namespace = metadataMappings[dsn]['NAMESPACE']
	# namespace = {"filemaker":"http://www.filemaker.com/xml/fmresultset"}
	layout = dataSourceAccessDetails['dataSourceLayout']
	server = dataSourceAccessDetails['dataSourceIP']
	user = dataSourceAccessDetails['dataSourceUsername']
	password = dataSourceAccessDetails['dataSourceCredentials']

	if len(idNumber) <= 5:
		requestURL = (
		"http://{0}/fmi/xml/fmresultset.xml?"
		"-db={1}&-lay={2}"
		"&AccessionNumberItemNumber=={3}"
		"&-find".format(server, dsn, layout,idNumber)
		)
		print(requestURL)
	elif len(idNumber) == 9:
		requestURL = (
		"http://{0}/fmi/xml/fmresultset.xml?"
		"-db={1}&-lay={2}"
		"&Barcode={3}"
		"&-find".format(server, dsn, layout,idNumber)
		)
	else:
		pass

	# print(requestURL)
	xml = requests.get(requestURL,auth=(user,password))
	recordDict = metadataMaster.metadataMasterDict
	root = etree.fromstring(xml.text.encode())
	#print(root)
	# THERE SHOULD ONLY EVER BE ONE RECORD IN A RESULTSET 
	# SINCE ITEM NUMBERS SHOULD BE UNIQUE
	recordElement = root.find(
		"./filemaker:resultset/filemaker:record",
		namespace
		)
	#print(recordElement)
	# do a little back and forth to get a new root 
	# that is just the single <record> element
	recordString = etree.tostring(recordElement)
	recordRoot = etree.fromstring(recordString)

	for fieldName, details in metadataMappings[dsn]['FIELDS'].items():
		for _,sourceFieldName in details.items():
			xpathExpression = "./filemaker:field[@name='{}']".format(
				sourceFieldName
				)
			fieldResult = recordRoot.find(xpathExpression,namespace)
			recordDict[fieldName] = fieldResult[0].text

	for key,value in recordDict.items():
		if value == None:
			recordDict[key] = ""
		else:
			#print(type(value))
			pass

	# print("THIS IS THE RECORD DICT FROM FMQUERY")
	# print(recordDict)
	return recordDict
