SQLALCHEMY_DATABASE_URI = 'mysql://admin:pass@localhost/db_name'

SECRET_KEY = 'bloop'
WTF_CSRF_SECRET_KEY= "bleep"
SHARED_DIR = 'blop'
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