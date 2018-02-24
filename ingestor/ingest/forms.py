from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ingestForm(FlaskForm):
	runIngest = BooleanField('Ingest?')
	target = StringField("targetObject")
	doProres = BooleanField("make prores?")
	proresToDave = BooleanField("deliver prores to dave?")
	doConcat = BooleanField("concatenate reels?")
