#!/usr/bin/env python3

import sys
sys.path.insert(0, '/Users/RLAS_Admin/Sites/ingest/login')

import json, hashlib, os, os.path, re, urllib.parse, chardet
import pyodbc

from login import login

basename = sys.argv[1]

# print(basename)

idRegex = re.compile(r'(.+\_)(\d{5})(\_.*)')
idMatch = re.match(idRegex, basename)
if not idMatch == None: 
	idNumber = idMatch.group(2)
	idNumber = idNumber.lstrip("0")
else:
	idNumber = "00000"

print(idNumber+"<br/><br/>")

def query(idNumber):
	destination = "filemaker"
	user = login(destination)[0]
	cred = login(destination)[1]
	# print("querying")
	# OPEN CONNECTION TO FILEMAKER DATABASE WITH DESCRIPTIVE METADATA

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
	# for row in rows:
	# 	print(row, chardet.detect(row[0].encode()))
	resultData = {}	
	resultList = [x for y in rows for x in y]
	# print(resultList)
	
	# A NULL RESULT WILL YIELD AN EMPTY LIST, SO CHECK THAT SOMETHING WAS FOUND, OR SKIP THE FILE. 
	# IF I SET UP LOGGING THIS SHOULD BE LOGGED FOR SURE.
	if not resultList == []:
		valueDict = { "title" : resultList[0],
			"altTitle" : resultList[1],
			"accPref" : resultList[2],
			"accDepos" : resultList[3],
			"accItem" : resultList[4],
			"projGroup" : resultList[5],
			"country" : resultList[6],
			"year" : int(resultList[7]),
			"directors" : resultList[8],
			"credits" : resultList[9],
			"notes" : resultList[10],
			"condition" : resultList[11]
			}

		for key,value in list(valueDict.items()):
			print(valueDict[key])
			if value == None:
				valueDict[key] = "--"

		# resultData[8] = valueDict["title"]
		# resultData[86] = valueDict["altTitle"]
		# resultData[87] = valueDict["accPref"]
		# resultData[88] = valueDict["accDepos"]
		# resultData[89] = valueDict["accItem"]
		# resultData[90] = valueDict["projGroup"]
		# resultData[91] = valueDict["country"]
		# resultData[92] = valueDict["year"]
		# resultData[93] = valueDict["directors"]
		# resultData[94] = valueDict["credits"]
		# resultData[95] = valueDict["notes"]
		# resultData[96] = valueDict["condition"]

		# print(valueDict)
		# return valueDict
		resultJSON = json.dumps(valueDict)
		# print(resultJSON)
		return resultJSON
		# return "FUCK YOU"

	# IF THERE IS NOTHING IN THE DATABASE TRY PASSING THE FILE WITH NULL VALUES OTHER THAN THE FILENAME AS 'TITLE'
	# 
	# I WILL WANT TO CONSIDER BOTH TIMES WHEN THERE IS AN ERROR IN THE DB QUERY *AND* TIMES WHERE THE FILE
	# IS NOT FROM THE FILM COLLECTION AND ISN'T EXPECTED TO HAVE A FILEMAKER RECORD
	else:
		print("*"*50+"THERE IS NO RECORD MATCHING "+basename+" IN THE DATABASE.\n\nPLEASE CHECK THE FILENAME OR THE DATABASE IF YOU THINK THIS IS WRONG."+"*"*50)
		resultData['title'] = [basename]
		resultJSON = json.dumps(resultData)

		return resultJSON

query(idNumber)