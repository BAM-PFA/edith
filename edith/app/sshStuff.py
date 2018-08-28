#!/usr/bin/env python3
'''
Defines a class to connect to a remote server and do stuff there.
'''
# standard library
import os
# nonstandard libraries
from paramiko import client

class connect:
	client = None

	def __init__(self, address, username, key_filename):
		print('connecting to {} ...'.format(address))
		self.client = client.SSHClient()
		self.client.set_missing_host_key_policy(client.AutoAddPolicy())
		self.client.connect(address, username=username, key_filename=key_filename)
		print("connected ....")

	def sendCommand(self, command):
		if(self.client):
			try:
				stdin, stdout, stderr = self.client.exec_command(command)
				return stdout
			except:
				return "There was an error in the remote command."

		else:
			print("No connection")
