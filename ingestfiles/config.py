import os
from instance import config as instance

SHARED_DIR = instance.SHARED_DIR
KNOWN_USERS = instance.KNOWN_USERS
DB_CONNECTIONS = instance.DB_CONNECTIONS
REMOTE_CONNECTIONS = instance.REMOTE_CONNECTIONS
# DEFAULT_REMOTE_NAME = instance.DEFAULT_REMOTE_NAME

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
	'REMOTE_CONNECTIONS': REMOTE_CONNECTIONS
}
