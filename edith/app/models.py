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
	IPaddress = db.Column(db.String(60), unique=True)
	# account with access 
	username = db.Column(db.String(60), unique=True)
	# account credentials
	credentials = db.Column(db.String(60), unique=True)
	description = db.Column(db.String(200))

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
	fieldUniqueName = db.Column(db.String(60), unique=True)
	# data source
	dataSource = db.Column(db.String(60))
	# resourceSpace field ID # 
	rsFieldID = db.Column(db.Integer, unique=True)
	description = db.Column(db.String(200))
