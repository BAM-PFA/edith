#!/usr/bin/env python3
# standard library modules
import ast
from multiprocessing.dummy import Pool as ThreadPool
import os
import re
import subprocess
import sys
from time import sleep
# non-standard libraries
from flask import render_template, request
import wtforms
# local modules
from .. import utils


def get_aip_human_name(aipPath):
	'''
	ALERT: THIS IS A HACK!!!
	Peer into the UUID named AIP and look for the PBCore XML file for the asset,
	which *should* be named after the canonical name of the ingested object.
	Then return this human-readable name so that it can be listed for writing 
	to LTO. 
	It is 100 percent possible/likely that this is a dumb way of finding
	what we are looking for, but it's a quick&dirty solution that should also
	mostly work.
	'''
	# init humanName as False in preparation for failure
	humanName = False
	if os.path.exists(aipPath):
		# going to assume that the AIP follows the current structure for this
		# so there is a parent dir named after the ingest UUID
		# and under that there is a metadata dir and in that is the pbcore 
		# xml file that contains the human-readable name that we want
		UUID = os.path.basename(aipPath)
		metadataDir = os.path.join(aipPath,UUID,'metadata')
		if os.path.exists(metadataDir):
			for thing in os.listdir(metadataDir):
				if "_pbcore.xml" in thing:
					# GRAB THE HUMAN NAME
					humanName = thing.replace("_pbcore.xml","")
				else:
					print("THERE IS NO PBCORE XML FILE FOR THIS OBJECT!!")
		else:
			print("there is no metadata dir in the AIP??")
			
	else:
		print(
			"the aip path you provided ({}) does not exist.".format(aipPath)
			)

	return humanName

def run_ltfs(devname,tempdir,mountpoint):
	command = (
		"sudo ltfs "
		"-o gid=33 "
		"-o uid=33 "
		"-o work_directory={} "
		"-o noatime "
		"-o capture_index "
		"-o devname={} "
		"{}".format(tempdir,devname,mountpoint)
		)
	commandList = command.split()
	print(commandList)
	doit = subprocess.Popen(
		commandList,
		stdin=subprocess.DEVNULL,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.PIPE,
		close_fds=True
		)
	for line in doit.stderr.read().splitlines():
		print(line.decode())

	return doit.stderr

# MOVE THIS TO UTILS AND RENAME IT FOLDER_SIZE()
def aip_size(path):
	'''
	Stolen from https://stackoverflow.com/q/40840037
	'''
	total = 0
	for entry in os.scandir(path):
		if entry.is_file():
			total += entry.stat().st_size
		elif entry.is_dir():
		   total += aip_size(entry.path)
	return total

def LTO_free_space(mountpoint):
	'''
	Get the free space left on an LTO tape and return the value in bytes`
	'''
	output = subprocess.run(['df',mountpoint],stdout=subprocess.PIPE)
	dfLine = output.stdout.decode().splitlines()[1]
	# should look like:
	# "ltfs:/dev/nst1 # mountpoint
	# 5597795328  # 1K-blocks
	# 6144 # used
	# 5597789184  # available
	# 1% # Use%
	# /path/to/mtn/point/18051B" # mounted on
	if dfLine.startswith('ltfs'):
		bytesAvailable = dfLine.split()[3]
		return int(bytesAvailable)
	else:
		return 0

# this file size calc came from:
# http://stackoverflow.com/questions/14996453/python-libraries-to-calculate-human-readable-filesize-from-bytes
# MOVE THIS TO UTILS.PY
def humansize(nbytes):
	suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
	if nbytes == 0:
		return '0 B'
	i = 0
	while nbytes >= 1024 and i < len(suffixes)-1:
		nbytes /= 1024.
		i += 1
	f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
	return '%s %s' % (f, suffixes[i])
