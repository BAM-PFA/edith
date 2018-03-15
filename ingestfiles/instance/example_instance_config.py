# SQLALCHEMY_DATABASE_URI = 'mysql://admin:pass@localhost/db_name'

SECRET_KEY = 'bloop'
WTF_CSRF_SECRET_KEY= "bleep"

# there can only be one entry for shared directory. 
# 'my host' should either be localhost or 
# map to a 'my server' name in REMOTE_CONNECTIONS
# the path should be the full path on the host machine
SHARED_DIR = {
	'my directory':{
		'host name':'my host',
		'host IP address':'1.2.3.4',
		'directory full path':'/full/path/to/my/dir'
		}
}

# SETTING SECRET STUFF HERE IN CONFIG DICTS 
# SINCE WE ONLY HAVE A FEW USERS AND IT'S NOT
# WORTH IT TO BUILD A DATABASE FOR LIKE 3 THINGS
KNOWN_USERS = {
	'defaultUser':{
		'fullname':'Default P. User',
		'RSuserName':'Default',
		'resourcespaceKey':'123456789'
		}
	}

DB_CONNECTIONS = {
	'my_database':{
		'dsn':'my_db_dsn',
		'server':'my_db_server',
		'accountName':'my_ingest_user',
		'password':'my_ingest_user_pass'
		}
	}

# MUST MATCH A KEY IN REMOTE_CONNECTIONS
DEFAULT_REMOTE_NAME = 'my server'
REMOTE_CONNECTIONS = {
	'my server':{
		'address':'1.2.3.4',
		'username':'my_username',
		'password':'my_password',
		'ssh private key file':'~/.ssh/id_rsa'
		}
}
