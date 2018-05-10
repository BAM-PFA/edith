from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired

class LTO_id_form(FlaskForm):
	"""
	Enter a value for the LTO tape in the A drive
	"""
	tapeAid = wtforms.StringField('Please enter a valid ID for LTO tape A: ')
	submit = wtforms.SubmitField('Submit')

class format_form(FlaskForm):
	"""
	Action to format LTO tapes in A and B drives
	"""	
	submit = wtforms.SubmitField('FORMAT TAPES!!')

class mount(FlaskForm):
	"""
	Action to mount formatted LTO tapes in A and B drives
	"""	
	tapeBarcodes = wtforms.HiddenField('tapeBarcodes')
	submit = wtforms.SubmitField('MOUNT TAPES!!')

class aip_object_form(FlaskForm):
	"""
	Fields for an individual AIP
	"""
	# this is the full path to the individual AIP
	targetPath = wtforms.HiddenField('targetPath')
	# this is the human readable name for the AIP
	targetBase = wtforms.HiddenField('targetBase')
	writeToLTO = wtforms.BooleanField('Write to tape?',default='')

class write_to_LTO(FlaskForm):
	'''
	General input form
	'''
	suchChoices = wtforms.HiddenField(default='default choices')
	submit = wtforms.SubmitField('WRITE TO LTO')
