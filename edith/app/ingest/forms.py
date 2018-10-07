from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Email

class MetadataForm(FlaskForm):
        '''
        Fields for additional metadata
        '''
        metadataTest1 = wtforms.StringField("one metadata?",default='')
        metadataTest2 = wtforms.StringField("two metadata?",default='')

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
	metadataForm = wtforms.FormField(MetadataForm)
	#metadataFields = wtforms.FieldList(StringField('metadata1'))

class IngestForm(FlaskForm):
	'''
	General input form
	'''
	suchChoices = wtforms.HiddenField(default='default choices')
	user = wtforms.StringField('Please enter your email address:',validators=[DataRequired(), Email()])
	submit = wtforms.SubmitField('Submit')
