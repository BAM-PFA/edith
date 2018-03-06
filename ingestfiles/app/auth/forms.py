from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = wtforms.StringField('Username', validators=[DataRequired()])
	password = wtforms.PasswordField('Password', validators=[DataRequired()])
	remember_me = wtforms.BooleanField('Remember Me')
	submit = wtforms.SubmitField('Sign In')

