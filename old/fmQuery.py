#!/usr/bin/env python3

import json, hashlib, os, os.path, re, urllib.parse, subprocess
import pyodbc



def query(idNumber,basename):
	
	# OPEN CONNECTION TO FILEMAKER DATABASE WITH DESCRIPTIVE METADATA

	c = pyodbc.connect("DRIVER={FileMaker ODBC};DATABASE=PFA_Collection;SERVER=bampfa-pfm13.ist.1918.berkeley.edu;UID=resourcespace;PWD=mediaarchive2017")
	c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
	c.setencoding(encoding='utf-8')
	cursor= c.cursor()
	
	# SQL TO GET REQUIRED METADATA VALUES FROM FM
	# SQL TO GET REQUIRED METADATA VALUES FROM FM
	cursor.execute("SELECT m_245a_CompleteTitle FROM CollectionItem WHERE AccessionNumberItemNumber = ?",idNumber)	
	# for row in cursor.tables():
	# 	print(row.table_name)	

	rows = cursor.fetchall()
	resultData = {}	
	resultList = [x for y in rows for x in y]
	# print(resultList)
	
	# A NULL RESULT WILL YIELD AN EMPTY LIST, SO CHECK THAT SOMETHING WAS FOUND, OR SKIP THE FILE. 
	# IF I SET UP LOGGING THIS SHOULD BE LOGGED FOR SURE.
	if not resultList == []:
		resultData[84] = resultList[0]
		# resultData[8] = resultList[1]
		# format = resultList[0]
		# date_ingested = resultList[1]

		resultJSON = json.dumps(resultData)
		# print(resultJSON)
		quotedJSON = urllib.parse.quote(resultJSON.encode())
		
		return quotedJSON

	# IF THERE IS NOTHING IN THE DATABASE TRY PASSING THE FILE WITH NULL VALUES OTHER THAN THE FILENAME AS 'TITLE'
	# 
	# I WILL WANT TO CONSIDER BOTH TIMES WHEN THERE IS AN ERROR IN THE DB QUERY *AND* TIMES WHERE THE FILE
	# IS NOT FROM THE FILM COLLECTION AND ISN'T EXPECTED TO HAVE A FILEMAKER RECORD
	else:
		print("*"*50+"THERE IS NO RECORD MATCHING "+basename+" IN THE DATABASE.\n\nPLEASE CHECK THE FILENAME OR THE DATABASE IF YOU THINK THIS IS WRONG."+"*"*50)
		resultData[84] = [""]
		resultData[8] = [basename]
		resultJSON = json.dumps(resultData)
		# print(resultJSON)
		quotedJSON = urllib.parse.quote(resultJSON.encode())

		return quotedJSON
