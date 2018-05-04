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
	submit = wtforms.SubmitField('MOUNT TAPES!!')