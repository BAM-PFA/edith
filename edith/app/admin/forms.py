from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, User


class DepartmentForm(FlaskForm):
	"""
	Form for admin to add or edit a department
	"""
	deptname = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Submit')

class AddUserForm(FlaskForm):
	"""
	Form for admin to create or edit users
	"""
	department_id = QuerySelectField(
		query_factory=lambda: Department.query.all(),
        get_pk=lambda x: x.id,
		get_label="deptname"
		)
	email = StringField('email address', validators=[DataRequired(),Email()])
	username = StringField('username', validators=[DataRequired()])
	first_name = StringField('First name', validators=[DataRequired()])
	last_name = StringField('Last name', validators=[DataRequired()])
	RSusername = StringField('ResourceSpace username', validators=[DataRequired()])
	RSkey = StringField('ResourceSpace API key', validators=[DataRequired()])
	is_admin = BooleanField('Admin?')
	password = PasswordField('Password', validators=[EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')

	submit = SubmitField('Submit')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')

class EditUserForm(FlaskForm):
    """
    Form for admin to create or edit users
    """
    department_id = QuerySelectField(
        query_factory=lambda: Department.query.all(),
        get_label="deptname"
        )
    email = StringField('email address', validators=[DataRequired(),Email()])
    username = StringField('username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    RSusername = StringField('ResourceSpace username', validators=[DataRequired()])
    RSkey = StringField('ResourceSpace API key', validators=[DataRequired()])
    is_admin = BooleanField('Admin?')
    password = PasswordField('Password', validators=[EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')

    submit = SubmitField('Submit')

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email is already in use.')