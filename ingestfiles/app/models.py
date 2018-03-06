from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class IngestUser(UserMixin, db.Model):
	'''
	Create a table for Ingestfiles users
	'''

	__tablename__ = 'ingestusers'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50),index=True, unique=True)
	password_hash = db.Column(db.String(128))
	resourcespace_id = db.Column(db.Integer, db.ForeignKey('rsusers.id'))
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


class RSuser(db.Model):
	'''
	Create a table for RS entities
	'''
	__tablename__ = 'rsusers'

	id = db.Column(db.Integer, primary_key=True)
	rs_email = db.Column(db.String(50), unique=True)
	rs_key = db.Column(db.String(64), unique=True)

	def __repr__(self):
		return '<RS User: {}>'.format(self.rs_email)
