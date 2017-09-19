#!/usr/bin/env python3

import requests, pyodbc, json, hashlib, os, os.path, re, urllib, subprocess, paramiko, time

# SET THE SOURCE FOLDER FOR WHERE TO LOOK FOR RESOURCESPACE ASSETS
resourceOutFolder = "/Users/bampfa/Desktop/mediaMicroservicesTrial/outdir/resourcespace_output/"

def login(destination):
	with open("stuff.txt","r") as credentialFile:
		credentialJSON = json.loads(credentialFile.read())
		desiredUser = [x["user"] for x in credentialJSON if x["host"] == destination]
		desiredCred = [y["pass"] for y in credentialJSON if y["host"] == destination]
	return [desiredUser[0],desiredCred[0]]

def query(idNumber,basename):
	
	# OPEN CONNECTION TO FILEMAKER DATABASE WITH DESCRIPTIVE METADATA
	c = pyodbc.connect("DRIVER={FileMaker ODBC};DSN=mmTest;SERVER=localhost;UID=michael;PWD=michael")
	c.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
	c.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
	c.setencoding(encoding='utf-8')
	cursor= c.cursor()
	
	# SQL TO GET REQUIRED METADATA VALUES FROM FM
	cursor.execute("""
		
		SELECT summary, tilte FROM microservicesTrial WHERE original_accession_number = ?

		""",idNumber)
	
	rows = cursor.fetchall()
	resultData = {}	
	resultList = [x for y in rows for x in y]
	# print(resultList)
	
	# A NULL RESULT WILL YIELD AN EMPTY LIST, SO CHECK THAT SOMETHING WAS FOUND, OR SKIP THE FILE. 
	# IF I SET UP LOGGING THIS SHOULD BE LOGGED FOR SURE.
	if not resultList == []:
		resultData[84] = resultList[0]
		resultData[8] = resultList[1]
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
		print("THERE IS NO RECORD MATCHING THIS FILE IN THE DATABASE, PLEASE CHECK THE FILENAME OR THE DATABASE AND TRY AGAIN.")
		resultData[84] = [""]
		resultData[8] = [basename]
		resultJSON = json.dumps(resultData)
		# print(resultJSON)
		quotedJSON = urllib.parse.quote(resultJSON.encode())

		return quotedJSON

def resourceSpaceAPIcall(metadata,filePath):
	destination = "resourcespace"
	user = login(destination)[0]
	cred = login(destination)[1]

	query = "user="+user+"&function=create_resource_from_local&param1=3&param2=0&param3="+filePath+"&param4=&param5=&param6=&param7="+metadata
	sign = hashlib.sha256(cred.encode()+query.encode())
	signDigest = sign.hexdigest()
	
	destination = "red"
	user = login(destination)[0] 
	cred = login(destination)[1]

	completePOST = 'http://'+user+':'+cred+'@10.253.22.21:/~'+user+'/resourcespace/api/?'+query+"&sign="+signDigest
	print(completePOST)
	
	try:
		resp = requests.post(completePOST)
		# print(resp.text)
	except ConnectionError as err:
		print("OOPS "*25)
		raise err

	print(resp.status_code)


def ingestToResourceSpace(resource, basename):
	print(resource)
	idRegex = re.compile(r'(.+\_)(\d{5})(\_.*)')
	idMatch = re.match(idRegex, basename)
	if not idMatch == None:
		idNumber = idMatch.group(2)
		# print(idNumber)
	else:
		idNumber = ""
	
	# GET SSH CREDENTIALS
	destination = "red"
	targetDir = "/Users/RLAS_Admin/Sites/resourceTarget/"
	targetFile = targetDir+basename
	quotedPath = urllib.parse.quote(targetFile, safe='')
	
	# OPEN SSH & SFTP THE FILE
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	user = login(destination)[0]
	cred = login(destination)[1]
	try:
	    ssh.connect('10.253.22.21', username=user,
	        password=cred)
	    sftp = ssh.open_sftp()
	    sftp.chdir(targetDir)
	    try:
	        sftp.put(resource, targetFile)
	        
	    except IOError:
	        print('Transfer failed at sftp step.')
	        
	    ssh.close()
	except paramiko.SSHException:
	    print("Connection Error")

	# ONCE THE FILE IS SFTP'ED WE CAN PUT IN THE API CALL
	resourceSpaceAPIcall(query(idNumber,basename),quotedPath)

#########################################
#                                       #
# THIS IS WHERE USER INTERACTION BEGINS #
#                                       #
#########################################

ingestFolder = input("Drag the folder you want to ingest here: ").rstrip()
# resourceSpaceStagingFolder = "/Users/bampfa/Sites/localFiles/"

# ASK FOR INGESTER ID; THIS IS USED BY ingestfile FOR ENTRY INTO THE MEDIAMICROSERVICES MYSQL DB
authorized_users = ['shibata@berkeley.edu','davetaylor@berkeley.edu','gibbscman@berkeley.edu','mcq@berkeley.edu']
user = input("Hello, what is your email address? ")

if not user in authorized_users:
	print("Sorry, you didn't enter a recognized email address. Try again!")
	quit()

# PROCESS THE FILE WITH MEDIA MICROSERVICES
for item in os.listdir(ingestFolder):
	print(item)
	if not item.startswith("."):
		filePath = os.path.abspath(ingestFolder+"/"+item)
		fileNameForMediaID = os.path.splitext(item)[0]
		try:
			subprocess.call(['ingestfile','-e','-u',user,'-I',filePath,'-m',fileNameForMediaID])
		except IOError as err:
			print("OS error: {0}".format(err))

# THIS IS WHERE A CALL TO mountlto / writelto WILL HAPPEN. [ writelto(path/to/AIP) ]
# FUNCTION SHOULD RETURN ORIGINAL FILENAME AND LTO TAPE ID
# THEN IT CAN CALL ANOTHER API UPDATE TO THE RESOURCESPACE RECORD AND ADD LTO ID NUMBER
# PER DAVE, ALSO MAYBE MAKE A .TAR OF A DPX SEQUENCE?

for resource in os.listdir(resourceOutFolder):
	filePath = resourceOutFolder+resource
	if os.path.isfile(filePath):
		if not resource.startswith("."):
			ingestToResourceSpace(filePath,resource)

#
# CLEANUP SHOULD HAPPEN HERE: CLEAN OUT THE RESOURCESPACEOUT FOLDER UNDER MM; REMOVE ANY AIPs IN MM
# THAT WERE SUCCESSFULLY WRITTEN TO LTO; HOW TO CHECK?? CHECKSUM??
