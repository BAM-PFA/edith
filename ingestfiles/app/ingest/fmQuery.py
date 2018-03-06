#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

import json
import hashlib
import os
import os.path
import re
import urllib.parse
import subprocess
import pyodbc
from login import login


def query(idNumber,filePath,basename):
	# THIS FIRST BIT USES mediainfo	TO GET THE DURATION OF THE VIDEO 
	# IT ISN'T NECESSARY BUT IT RETURNS THE VALUE IN A SLIGHTLY DIFFERENT
	# FORMAT THAN THE RESOURCESPACE DEFAULT....
	command = "mediainfo "+filePath
	mediainfo = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
	for line in mediainfo.stdout:
		print(line.decode())
		if 'Duration'  in line.decode():
			info = line.decode().rstrip().split(":")
			duration = info[1]

	destination = "filemaker"
	user = login(destination)[0]
	cred = login(destination)[1]
	print("querying")
	resultData = {}	
	# OPEN CONNECTION TO FILEMAKER DATABASE WITH DESCRIPTIVE METADATA
	# NOTE: I USED THE ODBC MANAGER GUI APPLICATION TO CONFIGURE THE DSN AS pfacolleciton AND THE ENCODING AS UTF-8
	
	try:
		c = pyodbc.connect("DRIVER={FileMaker ODBC};DSN=pfacollection;SERVER=bampfa-pfm13.ist.1918.berkeley.edu;UID="+user+";PWD="+cred)
		c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
		c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
		c.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
		c.setencoding(encoding='utf-8')
		cursor= c.cursor()
		
		# SQL TO GET REQUIRED METADATA VALUES FROM FM
		cursor.execute("""SELECT m_245a_CompleteTitle, AlternativeTitle, 
			AccessionNumberPrefix, AccessionNumberDepositorNumber, 
			AccessionNumberItemNumber, ProjectGroupTitle,
			m_257a_Country, m_260c_ReleaseYear,
			ct_DirectorsNames, Credits,
			GeneralNotes, m_945z_GeneralConditionNotes
			FROM CollectionItem WHERE AccessionNumberItemNumber = ?""",idNumber)	
		rows = cursor.fetchall()
		
		origResultList = [x for y in rows for x in y]
	except:
		origResultList = []
	# print(resultList)
	
	# A NULL RESULT WILL YIELD AN EMPTY LIST, SO CHECK THAT SOMETHING WAS FOUND, OR SKIP THE FILE. 
	# IF I SET UP LOGGING THIS SHOULD BE LOGGED FOR SURE.
	if not origResultList == []:
		resultList = [str(item).replace("\r"," ") for item in origResultList]

		valueDict = { "title" : resultList[0],
			"altTitle" : resultList[1],
			"accPref" : resultList[2],
			"accDepos" : resultList[3],
			"accItem" : resultList[4],
			"fullAcc" : ''.join(resultList[2:5]),
			"projGroup" : resultList[5],
			"country" : resultList[6],
			"year" : resultList[7].rstrip(".0"),
			"directors" : resultList[8],
			"credits" : resultList[9],
			"notes" : resultList[10],
			"condition" : resultList[11]
			}
		for key,value in list(valueDict.items()):
			if type(value) == str:
				value.replace("\r"," ")
				value.replace("\n"," ")
			# elif type(value) == float:
				# value = str(int(value))
			else:
				if value == None:
					valueDict[key] = "--"

		resultData[8] = valueDict["title"]
		resultData[86] = valueDict["altTitle"]
		resultData[87] = valueDict["accPref"]
		resultData[88] = valueDict["accDepos"]
		resultData[89] = valueDict["accItem"]
		resultData[99] = valueDict["fullAcc"]
		resultData[90] = valueDict["projGroup"]
		resultData[91] = valueDict["country"]
		resultData[92] = valueDict["year"]
		resultData[93] = valueDict["directors"]
		resultData[94] = valueDict["credits"]
		resultData[95] = valueDict["notes"]
		resultData[96] = valueDict["condition"]
		resultData[100] = duration

		resultJSON = json.dumps(resultData)
		quotedJSON = urllib.parse.quote(resultJSON.encode())

		return quotedJSON

	# IF THERE IS NOTHING IN THE DATABASE TRY PASSING THE FILE WITH NULL VALUES OTHER THAN THE FILENAME AS 'TITLE'
	# 
	# I WILL WANT TO CONSIDER BOTH TIMES WHEN THERE IS AN ERROR IN THE DB QUERY *AND* TIMES WHERE THE FILE
	# IS NOT FROM THE FILM COLLECTION AND ISN'T EXPECTED TO HAVE A FILEMAKER RECORD
	else:

		resultData[8] = basename
		resultJSON = json.dumps(resultData)
		quotedJSON = urllib.parse.quote(resultJSON.encode())

		return quotedJSON
