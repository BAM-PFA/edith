from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired,Email

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
	# this is the size of the AIP:
	aipSize = wtforms.HiddenField('aipSize')
	aipHumanSize = wtforms.HiddenField('aipHumanSize')
	writeToLTO = wtforms.BooleanField('Write to tape?',default='')

class write_to_LTO(FlaskForm):
	'''
	General input form
	'''
	suchChoices = wtforms.HiddenField(default='default choices')
	user = wtforms.StringField('Please enter your email address:',validators=[DataRequired(), Email()])
	submit = wtforms.SubmitField('WRITE TO LTO')

# class unmount_lto(FlaskForm):
# 	'''
# 	Unmount LTO tapes
# 	'''
# 	tapeBarcodes = wtforms.HiddenField('tapeBarcodes')
# 	submit = wtforms.SubmitField('MOUNT TAPES!!')