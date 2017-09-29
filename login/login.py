#!/usr/bin/env python3

import json

def login(destination):
	# print("Logging in")
	with open("../stuff.txt","r") as credentialFile:
		credentialJSON = json.loads(credentialFile.read())
		desiredUser = [x["user"] for x in credentialJSON if x["host"] == destination]
		desiredCred = [y["pass"] for y in credentialJSON if y["host"] == destination]
	# print(desiredUser[0],desiredCred[0])
	return [desiredUser[0],desiredCred[0]]