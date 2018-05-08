#!/usr/bin/env python3
# standard library modules
import subprocess

class mountTape:
	def __init__(self, tapeID, deviceName,command=None):
		self.tapeID = tapeID
		self.deviceName = deviceName
		if command == None:
			command = []
		self.command = command
		print("I EXIST")

	def run_ltfs():
		self.run = subprocess.Popen(self.command,stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
		self.out,self.err = self.run.communicate()

	def stderr():
		self.stderr = self.err.splitlines()
		return self.stderr
