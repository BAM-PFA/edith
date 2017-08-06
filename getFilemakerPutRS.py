#!/usr/bin/env python3

import requests, pyodbc, json, hashlib, os, re, urllib

# print(os.getegid(),os.getgid())

def query(idNumber):
	c = pyodbc.connect("DRIVER={FileMaker ODBC};DSN=mmTest;SERVER=localhost;UID=michael;PWD=michael")
	c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
	c.setencoding(encoding='utf-8')
	cursor= c.cursor()
	cursor.execute("""
		SELECT summary, tilte FROM microservicesTrial WHERE original_accession_number = ?

		""",idNumber)
	rows = cursor.fetchall()

	resultData = {}

	resultList = [x for y in rows for x in y]

	resultData[85] = resultList[0]
	resultData[8] = resultList[1]

	format = resultList[0]
	date_ingested = resultList[1]

	resultJSON = json.dumps(resultData)
	print(resultJSON)
	quotedJSON = urllib.parse.quote(resultJSON.encode())
	
	return quotedJSON


def resourceSpaceAPIcall(metadata,filePath):
	# user = 'admin'
	# privateKey = '0dd7d02017750160a476733139313b9ce563790632baee41e3169152cd1017d2'
	query = "user=admin&function=create_resource&param1=3&param2=0&param3="+filePath+"&param4=&param5=&param6=&param7="+metadata
	print(query)
	sign = hashlib.sha256(b'0dd7d02017750160a476733139313b9ce563790632baee41e3169152cd1017d2'+query.encode())

	signDigest = sign.hexdigest()
	# print(sign)
	# sign = str(sign)
	temp = 'http://localhost/~bampfa/ResourceSpace/api/?'+query+"&sign="+signDigest
	print(temp)
	resp = requests.post('http://localhost/~bampfa/ResourceSpace/api/?'+query+"&sign="+signDigest)

	print(resp.text)

hostFolder = '/Users/bampfa/Desktop/testGetFilemakerPutRS/'
idRegex = re.compile(r'(.+\_)(\d{5})(\_.*)')

for item in os.listdir(hostFolder):
	if not item.startswith('.'):
		
		filePathForAPI = 'file:///Users/bampfa/Desktop/testGetFilemakerPutRS/'+item
		print(filePathForAPI)
		quotedPath = urllib.parse.quote(filePathForAPI, safe='')
		idMatch = re.match(idRegex, item)
		idNumber = idMatch.group(2)
		resourceSpaceAPIcall(query(idNumber),quotedPath)

