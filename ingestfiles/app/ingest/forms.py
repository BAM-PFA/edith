from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired

class ObjectForm(FlaskForm):
	"""
	Fields for an individual object
	"""
	targetPath = wtforms.HiddenField('objectPath')
	targetBase = wtforms.HiddenField('objectBase')
	runIngest = wtforms.BooleanField('Ingest?',default='')
	doProres = wtforms.BooleanField("make prores?",default='')
	proresToDave = wtforms.BooleanField("deliver prores to dave?",default='')
	doConcat = wtforms.BooleanField("concatenate reels?",default='')

class IngestForm(FlaskForm):
	'''
	General input form
	'''
	suchChoices = wtforms.HiddenField(default='default choices')
	user = wtforms.StringField('Please enter your email address:')
	submit = wtforms.SubmitField('Submit')
