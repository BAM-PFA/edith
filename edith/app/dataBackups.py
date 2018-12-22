#!/usr/bin/env python3
'''
Script to be available for backups.
Ideally will be run via `cron`
'''
# standard library stuff
import configparser
import os
import time
# local modules
import app

timestamp = time.strftime("%Y-%m-%dT%H-%M-%S")
config = app.app_config
backupPath = config["DATA_BACKUP_PATH"]
if not os.path.isdir(backupPath):
	os.mkdir(backupPath)
##########################
### pymm db backup #######
# read the pymm config file and find where the pymm log is stored
pymmPath = config["PYMM_PATH"]
pymmConfigPath = os.path.join(pymmPath,'pymmconfig','config.ini')
pymmConfig = configparser.SafeConfigParser()
pymmConfig.read(pymmConfigPath)
pymmLogDir =  pymmConfig['logging']['pymm_log_dir']
pymmLogPath = os.path.join(pymmLogDir,'pymm_log.txt')
pymmDBname = pymmConfig['database settings']['pymm_db']
# get a valid pymm db user who can perform the mysqldump
validDbUser = next(
		(user for user in pymmConfig.options('database users') \
			if not user=='user')
	)
dbUserPass = pymmConfig['database users'][validDbUser]
pymmDumpFilePath = os.path.join(backupPath,"pymm-"+timestamp+".sql")
mysqlDumpCommand = [
		"mysqldump",
		"-u",validDbUser,
		"-p",dbUserPass,
		"--routines","--triggers","--events"
		pymmDBname,
		">",pymmDumpFilePath
	]
