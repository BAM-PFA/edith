'''
# app/models.py
taken from 
https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one
'''
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
	'''
	Create a User table
	Attributes
	- username
	- email
	- full name
	- ResourceSpace API key
	- ResourceSpace username
	- password hash
	- department ID
	- is_admin
	'''

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)
	first_name = db.Column(db.String(60), index=True)
	last_name = db.Column(db.String(60), index=True)
	RSusername = db.Column(db.String(60), index=True, unique=True)
	RSkey = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
	is_admin = db.Column(db.Boolean, default=False)

	@property
	def password(self):
		"""
		Prevent pasword from being accessed
		"""
		raise AttributeError('password is not a readable attribute.')

	@password.setter
	def password(self, password):
		"""
		Set password to a hashed password
		"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Check if hashed password matches actual password
		"""
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Department(db.Model):
	"""
	Create a Department table
	"""

	__tablename__ = 'departments'

	id = db.Column(db.Integer, primary_key=True)
	deptname = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))
	users = db.relationship('User', backref='department',
								lazy='dynamic')

	def __repr__(self):
		return '<Department: {}>'.format(self.deptname)

class Path(db.Model):
	'''
	Define paths that will be used in config:
	- shared dir
	- pymm paths
	  - AIP staging
	  - out dir
	  - rs proxy path 
	'''
	__tablename__ = 'paths'

	id = db.Column(db.Integer, primary_key=True)
	fullPath = db.Column(db.String(60), unique=True)
	IPaddress = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))

class Data_Source(db.Model):
	'''
	Define external data sources:
	- Collection db
	- FileMaker layout name as applicable
	- login details
	'''

	__tablename__ = 'data_sources'

	id = db.Column(db.Integer, primary_key=True)
	# dsn (data source name)
	dbName = db.Column(db.String(60), unique=True)
	# layout name for filemaker
	fmpLayout = db.Column(db.String(60), unique=True)
	# server address
	IPaddress = db.Column(db.String(60))
	# namespace for XML/XPATH
	namespace = db.Column(db.String(60))
	# account with access 
	username = db.Column(db.String(60))
	# account credentials
	credentials = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))
	# primary asset identifier for queries to the source
	# this is the first field that queries should use to find an item
	primaryAssetID = db.Column(db.String(60))
	# secondary asset identifier in case
	# the first one returns null or is not declared
	secondaryAssetID = db.Column(db.String(60))
	# tertiary asset identifier
	# as a last resort
	tertiaryAssetID = db.Column(db.String(60))

	fields = db.relationship('Metadata_Field', backref='datasource',
								lazy='dynamic')

class Metadata_Field(db.Model):
	'''
	Define metadata fields:
	- with values from external databases
	- with values from user form input
	'''
	__tablename__ = 'metadata_fields'

	id = db.Column(db.Integer, primary_key=True)
	# User-visible field name (e.g. Record ID)
	fieldName = db.Column(db.String(100))
	# field unique name (e.g. recordID)
	fieldUniqueName = db.Column(db.String(60),unique=True)
	# field name in the data source
	fieldSourceName = db.Column(db.String(60))
	# category of field (Film coll, Event, General, etc.)
	fieldCategory = db.Column(db.String(100))
	# data source
	try:
		dataSource_id = db.Column(db.Integer, db.ForeignKey('data_sources.id'))
	except:
		dataSource_id = None
	# resourceSpace field ID # 
	rsFieldID = db.Column(db.Integer)
	description = db.Column(db.String(200))

class Tape(db.Model):
	'''
	Maintain the status of a current tape

	'''
	__tablename__ = 'tapes'

	id = db.Column(db.Integer, primary_key=True)
	# tape barcode e.g. 19091A or 19091B
	tapeBarcode = db.Column(db.String(10))
	# UUID
	tapeUUID = db.Column(db.String(100))
	# status: mounted or unmounted
	status = db.Column(db.String(100))
	# date the tape was formatted with LTFS
	formattedDate = db.Column(db.DateTime)
	# mountpoint for the logical file system
	mountpoint = db.Column(db.String(100))
	# space remaining on the tape
	spaceAvailable = db.Column(db.Integer)

class TapeID(db.Model):
	'''
	Track the current Tape ID in use
	'''
	__tablename__ = 'tape_ids'

	id = db.Column(db.Integer, primary_key=True)
	a_version = db.Column(db.String(50))
	b_version = db.Column(db.String(50))
	