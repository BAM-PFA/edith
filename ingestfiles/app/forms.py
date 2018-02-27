from flask_wtf import FlaskForm
import wtforms,uuid
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = wtforms.StringField('Username', validators=[DataRequired()])
	password = wtforms.PasswordField('Password', validators=[DataRequired()])
	remember_me = wtforms.BooleanField('Remember Me')
	submit = wtforms.SubmitField('Sign In')

class ObjectForm(FlaskForm):
	"""
	Fields for an individual object
	"""
	targetPath = wtforms.HiddenField('objectPath')
	targetBase = wtforms.HiddenField('objectBase')
	runIngest = wtforms.BooleanField('Ingest?')
	doProres = wtforms.BooleanField("make prores?")
	proresToDave = wtforms.BooleanField("deliver prores to dave?")
	doConcat = wtforms.BooleanField("concatenate reels?")
	uuid = wtforms.HiddenField(str(uuid.uuid4()))

class IngestForm(FlaskForm):
	'''
	General input form
	'''
	choicesDict = {}
	targetObject = wtforms.FormField(ObjectForm)
	submit = wtforms.SubmitField('Submit')
