#!/usr/bin/env python3
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
import app

def xml_query(idNumber):
	namespace = {"filemaker":"http://www.filemaker.com/xml/fmresultset"}
	dsn = app.app_config["DB_CONNECTIONS"]["filemaker"]["dsn"]
	layout = app.app_config["DB_CONNECTIONS"]["filemaker"]["layout"]
	server = app.app_config["DB_CONNECTIONS"]["filemaker"]["server"]
	user = app.app_config["DB_CONNECTIONS"]["filemaker"]["accountName"]
	password = app.app_config["DB_CONNECTIONS"]["filemaker"]["password"]

	if len(idNumber) <= 5:
		requestURL = (
		"http://{0}/fmi/xml/fmresultset.xml?"
		"-db={1}&-lay={2}"
		"&AccessionNumberItemNumber={3}"
		"&-find".format(server, dsn, layout,idNumber)
		)
		# print(requestURL)
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
	recordDict = metadataMaster.metadata
	root = etree.fromstring(xml.text.encode())
	#print(root)
	# THERE SHOULD ONLY EVER BE ONE RECORD IN A RESULTSET SINCE ITEM NUMBERS SHOULD BE UNIQUE
	recordElement = root.find("./filemaker:resultset/filemaker:record",namespace)
	#print(recordElement)
	# do a little back and forth to get a new root that is just the single <record> element
	recordString = etree.tostring(recordElement)
	recordRoot = etree.fromstring(recordString)

	# BUILD OUT THE DICT WITH VALUES FROM THE FILEMAKER RESULT
	# uh, redo this with an iterator... 
	titleField = recordRoot.find("./filemaker:field[@name='m_245a_CompleteTitle']",namespace)
	recordDict["title"] = titleField[0].text

	altTitleField = recordRoot.find("./filemaker:field[@name='AlternativeTitle']",namespace)
	recordDict["altTitle"] = altTitleField[0].text

	accPrefField = recordRoot.find("./filemaker:field[@name='AccessionNumberPrefix']",namespace)
	recordDict["accPref"] = accPrefField[0].text
	accDeposField = recordRoot.find("./filemaker:field[@name='AccessionNumberDepositorNumber']",namespace)
	recordDict["accDepos"] = accDeposField[0].text
	accItemField = recordRoot.find("./filemaker:field[@name='AccessionNumberItemNumber']",namespace)
	recordDict["accItem"] = accItemField[0].text
	recordDict["accFull"] = "{}-{}-{}".format(recordDict["accPref"],recordDict["accDepos"],recordDict["accItem"])

	projGrpField = recordRoot.find("./filemaker:field[@name='ProjectGroupTitle']",namespace)
	recordDict["projGrp"] = projGrpField[0].text

	countryField = recordRoot.find("./filemaker:field[@name='m_257a_Country']",namespace)
	recordDict["country"] = countryField[0].text

	releaseYearField = recordRoot.find("./filemaker:field[@name='m_260c_ReleaseYear']",namespace)
	recordDict["releaseYear"] = releaseYearField[0].text

	directorsNamesField = recordRoot.find("./filemaker:field[@name='ct_DirectorsNames']",namespace)
	recordDict["directorsNames"] = directorsNamesField[0].text

	creditsField = recordRoot.find("./filemaker:field[@name='Credits']",namespace)
	recordDict["credits"] = creditsField[0].text

	generalNotesField = recordRoot.find("./filemaker:field[@name='GeneralNotes']",namespace)
	recordDict["generalNotes"] = generalNotesField[0].text

	conditionNoteField = recordRoot.find("./filemaker:field[@name='m_945z_GeneralConditionNotes']",namespace)
	recordDict["conditionNote"] = conditionNoteField[0].text

	barcodeField = recordRoot.find("./filemaker:field[@name='Barcode']",namespace)
	recordDict["Barcode"] = barcodeField[0].text

	languageField = recordRoot.find("./filemaker:field[@name='m_546a_Language']",namespace)
	recordDict["language"] = languageField[0].text

	soundField = recordRoot.find("./filemaker:field[@name='SoundCharacteristics']",namespace)
	recordDict["soundCharacteristics"] = soundField[0].text

	colorField = recordRoot.find("./filemaker:field[@name='ColorCharacteristics']",namespace)
	recordDict["color"] = colorField[0].text

	trtField = recordRoot.find("./filemaker:field[@name='RunningTime']",namespace)
	recordDict["runningTime"] = trtField[0].text

	trtDescField = recordRoot.find("./filemaker:field[@name='RunningTimeDescription']",namespace)
	recordDict["frameRateTRTdetails"] = trtDescField[0].text

	mediumField = recordRoot.find("./filemaker:field[@name='m_245h_Medium']",namespace)
	recordDict["medium"] = mediumField[0].text

	dimensionsField = recordRoot.find("./filemaker:field[@name='m_300c_Dimensions']",namespace)
	recordDict["dimensions"] = dimensionsField[0].text

	videoformatField = recordRoot.find("./filemaker:field[@name='VideoFormat']",namespace)
	recordDict["videoFormat"] = videoformatField[0].text

	vidstdField = recordRoot.find("./filemaker:field[@name='VideoStandard']",namespace)
	recordDict["videoStandard"] = vidstdField[0].text


	for key,value in recordDict.items():
		if value == None:
			recordDict[key] = ""
		else:
			#print(type(value))
			pass

	# print("THIS IS THE RECORD DICT FROM FMQUERY")
	# print(recordDict)
	return recordDict
