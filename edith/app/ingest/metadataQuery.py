#!/usr/bin/env python3
'''
This function queries defined external metadata source(s)
and builds out a dict of fields and values that maps to Bampfa
ResourceSpace and PBCore mappings.
'''
# standard libraries
import ast
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
#from config import app_config
from .. import db
from ..models import Metadata_Field

def xml_query(_metadata,idNumber,dataSourceAccessDetails):
	dsn = dataSourceAccessDetails['dataSourceName']
	namespace = dataSourceAccessDetails['dataSourceNamespace']
	namespace = ast.literal_eval(namespace)
	layout = dataSourceAccessDetails['dataSourceLayout']
	server = dataSourceAccessDetails['dataSourceIP']
	user = dataSourceAccessDetails['dataSourceUsername']
	password = dataSourceAccessDetails['dataSourceCredentials']
	primaryAssetIDField = dataSourceAccessDetails['dataSourcePrimaryID']
	secondaryAssetIDField = dataSourceAccessDetails['dataSourceSecondaryID']
	tertiaryAssetIDField = dataSourceAccessDetails['dataSourceTertiaryID']

	if len(idNumber) <= 5:
		# primaryAssetID is a 5-digit record id
		requestURL = (
		"http://{0}/fmi/xml/fmresultset.xml?"
		"-db={1}&-lay={2}"
		"&{3}=={4}"
		"&-find".format(server, dsn, layout, primaryAssetIDField, idNumber)
		)
		# print(requestURL)
	elif len(idNumber) == 9:
		# secondary ID = 9-digit barcode
		# don't do an exact match since multiple barcodes get concatenated
		requestURL = (
		"http://{0}/fmi/xml/fmresultset.xml?"
		"-db={1}&-lay={2}"
		"&{3}={4}"
		"&-find".format(server, dsn, layout, secondaryAssetIDField, idNumber)
		)
	else:
		# tertiary ID = 10-character Filemaker ID
		requestURL = (
		"http://{0}/fmi/xml/fmresultset.xml?"
		"-db={1}&-lay={2}"
		"&{3}=={4}"
		"&-find".format(server, dsn, layout, tertiaryAssetIDField, idNumber)
		)

	print(requestURL)
	xml = requests.get(requestURL,auth=(user,password))
	# print(xml.text)

	# Get the metadata dict from the Metadata object
	recordDict = {k:v for k,v in _metadata.innerMetadataDict.items()}
	#print(recordDict)
	root = etree.fromstring(xml.text.encode())
	# print(root)
	# THERE SHOULD ONLY EVER BE ONE RECORD IN A RESULTSET 
	# SINCE ITEM NUMBERS SHOULD BE UNIQUE
	recordElement = root.find(
		"./filemaker:resultset/filemaker:record",
		namespace
		)
	# print(recordElement)

	# do a little back and forth to get a new root 
	# that is just the single <record> element
	recordString = etree.tostring(recordElement)
	recordRoot = etree.fromstring(recordString)

	for fieldName,_ in recordDict.items():
		# print(fieldName)
		field = Metadata_Field.query.filter_by(fieldUniqueName=fieldName).first()
		try:
			sourceFieldName = field.fieldSourceName
			xpathExpression = "./filemaker:field[@name='{}']".format(
				sourceFieldName
				)
			# print(xpathExpression)
			try:
				fieldResult = recordRoot.find(xpathExpression,namespace)
				recordDict[fieldName] = fieldResult[0].text
			except:
				recordDict[fieldName] = None
		except:
			pass

	print(_metadata.innerMetadataDict)
	print("THIS IS THE RECORD DICT FROM FILEMAKER QUERY")
	print(recordDict)
	return recordDict
