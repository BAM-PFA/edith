#!/usr/bin/env python3
# standard library modules
import ast
import json
from multiprocessing import Pool
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
	Peer into the UUID named AIP and find the PBCore XML file for the asset,
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
				# REDO THIS WITH GLOB
				if "_pbcore.xml" in thing:
					# GRAB THE HUMAN NAME
					humanName = thing.replace("_pbcore.xml","")
				else:
					pass
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
	# print(commandList)
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

def run_moveNcopy(aipPath,tapeMountpoint):
	pythonBinary = utils.get_python_path()
	pymmPath = utils.get_pymm_path()
	moveNcopyPath = os.path.join(pymmPath,'moveNcopy.py')
	command = (
		"{} {} "
		"-s "
		"-i {} "
		"-d {}".format(
			pythonBinary,
			moveNcopyPath,
			aipPath,
			tapeMountpoint
			)
		)

	commandList = command.split()
	print(commandList)
	runit = subprocess.run(
		commandList,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
		)
	for line in runit.stdout.splitlines():
		print(line.decode())
	for line in runit.stderr.splitlines():
		print(line.decode())

	return runit.stdout


def write_LTO(aipDict,user):
	aMount,bMount = get_tape_mountpoints()
	sipWriteTuples = []
	if not False in (aMount,bMount):
		for tapeMountpoint in (aMount,bMount):
			for path,stuff in aipDict.items():
				# get aip paths and tape mountponts 
				# to build multithreading commands for both tapes
				details = [path,tapeMountpoint]
				sipWriteTuples.append(details)
		#for tapeMountpoint in (aMount,bMount):
		#	for path,stuff in aipDict.items():
		#		out = run_moveNcopy(path,tapeMountpoint)
		#		print("did moveNcopy on "+path)
		#		print(out)

	print(sipWriteTuples)
	pool = Pool(2)
	pool.starmap(run_moveNcopy,sipWriteTuples)
	pool.close()
	#pass

def write_LTO_temp_stats():
	'''
	Save the stats on mounted tapes to a temp file for reading
	by various processes.
	This file gets deleted on unmounting tapes (after writes?)
	'''

	stats = {
		"A":{
			"mountpoint":"",
			"spaceAvailable":""
			},
		"B":{
			"mountpoint":"",
			"spaceAvailable":""
			}
		}
	dfProcess = subprocess.run(['df'],stdout=subprocess.PIPE)
	dfTape = [
		line.decode() for line in dfProcess.stdout.splitlines() 
		if '/dev/nst' in line.decode()
		]
	for line in dfTape:
		if '/dev/nst0' in line:
			stats["A"]["mountpoint"] = line.split()[5]
			stats["A"]["spaceAvailable"] = line.split()[3]
		elif '/dev/nst1' in line:
			stats["B"]["mountpoint"] = line.split()[5]
			stats["B"]["spaceAvailable"] = line.split()[3]

	tempDir = utils.get_temp_dir()
	statsJsonPath = os.path.join(tempDir,"tempTapeStats.json")
	try:
		with open(statsJsonPath,"x") as f:
			pass
		os.chmod(statsJsonPath,0o777)
		with open(statsJsonPath,"w") as f:
			json.dump(stats,f)
		return True
	except:
		print("couldn't write the temp tape stats file")
		return False

def get_tape_stats():
	tempDir = utils.get_temp_dir()
	statsJsonPath = os.path.join(tempDir,"tempTapeStats.json")
	try:
		with open(statsJsonPath,'r') as f:
			stats = json.load(f)
	except:
		try:
			with open(statsJsonPath,'r') as f:
				stats = f.read()
				stats = ast.literal_eval(stats)
		except:
			print("couldn't read the stats file or it doesn't exist")
			stats = "NO STATS AVAILABLE"

	return stats

def get_tape_mountpoints():
	stats = get_tape_stats()
	if not stats == "NO STATS AVAILABLE":
		aMount = stats["A"]["mountpoint"]
		bMount = stats["B"]["mountpoint"]
	else:
		aMount = bMount = False

	return aMount,bMount


def delete_tape_temp_stats():
	'''
	Run this on unmounting tapes
	'''
	tempDir = utils.get_temp_dir()
	statsJsonPath = os.path.join(tempDir,"tempTapeStats.json")
	if os.path.exists(statsJsonPath):
		try:
			os.remove(statsJsonPath)
			return True
		except:
			print("couldn't delete the temp tape stats file")
			return False
	else:
		return False


