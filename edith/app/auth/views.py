#!/usr/bin/env python3
# standard library modules
import re
# non-standard libraries
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
import wtforms
# local modules
import app

from . import auth
from . forms import LoginForm
from .. import db
from .. models import User

print(User)
print(db)


@auth.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Handle requests to the /login route
	Log a user in through the login form
	"""
	form = LoginForm()
	print(form.errors)
	if form.validate_on_submit():
		print("HI")
		# check whether user exists in the database and whether
		# the password entered matches the password in the database
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(
				form.password.data):
			# log user in
			login_user(user)

			# redirect to the dashboard page after login
			if user.is_admin:
				return redirect(url_for('home.admin_dashboard'))
			else:
				return redirect(url_for('home.dashboard'))

		# when login details are incorrect
		else:
			flash('Invalid email or password.')

	# load login template
	# print("HI HI HI")
	return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
	"""
	Handle requests to the /logout route
	Log an employee out through the logout link
	"""
	logout_user()
	flash('You have successfully been logged out.')

	# redirect to the login page
	return redirect(url_for('auth.login'))