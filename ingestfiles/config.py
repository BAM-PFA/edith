import os
from instance import config as instance

SHARED_DIR = instance.SHARED_DIR
KNOWN_USERS = instance.KNOWN_USERS
DB_CONNECTIONS = instance.DB_CONNECTIONS
REMOTE_CONNECTIONS = instance.REMOTE_CONNECTIONS
PYMM_PATH = instance.PYMM_PATH
PYTHON3_BINARY_PATH = instance.PYTHON3_BINARY_PATH
RESOURCESPACE_PROXY_DIR = instance.RESOURCESPACE_PROXY_DIR
RS_BASE_URL = instance.RS_BASE_URL

class Config(object):
	HELLO = True


class DevelopmentConfig(Config):
	"""
	Development configurations
	"""

	DEBUG = True
	SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
	"""
	Production configurations
	"""

	DEBUG = False

app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'SHARED_DIR': SHARED_DIR,
	'KNOWN_USERS': KNOWN_USERS,
	'DB_CONNECTIONS': DB_CONNECTIONS,
	'REMOTE_CONNECTIONS': REMOTE_CONNECTIONS,
	'PYMM_PATH':PYMM_PATH,
	'PYTHON3_BINARY_PATH':PYTHON3_BINARY_PATH,
	'RESOURCESPACE_PROXY_DIR':RESOURCESPACE_PROXY_DIR,
	'RS_BASE_URL':RS_BASE_URL
}
