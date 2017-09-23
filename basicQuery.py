#!/usr/bin/env python3

import json, sys, hashlib, os, os.path, re, urllib.parse
import pyodbc

from login.py import login

basename = sys.argv[1]

# print(basename)

idRegex = re.compile(r'(.+\_)(\d{5})(\_.*)')
idMatch = re.match(idRegex, basename)
if not idMatch == None: 
	idNumber = idMatch.group(2)
else:
	idNumber = "00000"

# print(idNumber+"<br/><br/>")

def query(idNumber):
	destination = filemaker
	user = login(destination)[0]
	cred = login(destination)[1]
	print("querying")
	# OPEN CONNECTION TO FILEMAKER DATABASE WITH DESCRIPTIVE METADATA

	c = pyodbc.connect("DRIVER={FileMaker ODBC};DATABASE=PFA_Collection;SERVER=bampfa-pfm13.ist.1918.berkeley.edu;UID="+user+";PWD="+cred)
	c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
	c.setencoding(encoding='utf-8')
	cursor= c.cursor()
	
	# SQL TO GET REQUIRED METADATA VALUES FROM FM
	cursor.execute("SELECT m_245a_CompleteTitle, m_260c_ReleaseYear FROM CollectionItem WHERE AccessionNumberItemNumber = ?",idNumber)	
	rows = cursor.fetchall()
	resultData = {}	
	resultList = [x for y in rows for x in y]
	if not resultList == []:
		resultData['title'] = resultList[0]
		resultData['Release Year'] = resultList[1]
		resultJSON = json.dumps(resultData)		
		print(resultJSON)
		return resultData

	# IF THERE IS NOTHING IN THE DATABASE TRY PASSING THE FILE WITH NULL VALUES OTHER THAN THE FILENAME AS 'TITLE'
	# 
	# I WILL WANT TO CONSIDER BOTH TIMES WHEN THERE IS AN ERROR IN THE DB QUERY *AND* TIMES WHERE THE FILE
	# IS NOT FROM THE FILM COLLECTION AND ISN'T EXPECTED TO HAVE A FILEMAKER RECORD
	else:
		print("*"*50+"THERE IS NO RECORD MATCHING "+basename+" IN THE DATABASE.\n\nPLEASE CHECK THE FILENAME OR THE DATABASE IF YOU THINK THIS IS WRONG."+"*"*50)
		resultData['title'] = [""]
		resultJSON = json.dumps(resultData)

		return resultJSON

query(idNumber)