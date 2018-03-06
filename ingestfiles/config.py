import os
from instance import config as instance

SHARED_DIR = instance.SHARED_DIR

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
	'SHARED_DIR': SHARED_DIR
}