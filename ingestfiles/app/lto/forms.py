from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired

class LTO_id_form(FlaskForm):
	"""
	Fields for an individual object
	"""
	tapeAid = wtforms.StringField('Please enter a valid ID for LTO tape A: ')
	submit = wtforms.SubmitField('Submit')

class IngestForm(FlaskForm):
	'''
	General input form
	'''
	suchChoices = wtforms.HiddenField(default='default choices')
	user = wtforms.StringField('Please enter your email address:',validators=[DataRequired(), Email()])
	submit = wtforms.SubmitField('Submit')
