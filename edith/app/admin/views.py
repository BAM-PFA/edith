#!/usr/bin/env python3
# non-standard libraries
from flask import render_template, request, flash, url_for
import wtforms
# local modules
import app

# from . import admin
# from forms import LoginForm
# from .. import db
# from ..models import User


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     """
#     Handle requests to the /login route
#     Log a user in through the login form
#     """
#     form = LoginForm()
#     if form.validate_on_submit():

#         # check whether user exists in the database and whether
#         # the password entered matches the password in the database
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is not None and user.verify_password(
#                 form.password.data):
#             # log employee in
#             login_user(employee)

#             # redirect to the dashboard page after login
#             return redirect(url_for('ingest.edith'))

#         # when login details are incorrect
#         else:
#             flash('Invalid email or password.')

#     # load login template
#     return render_template('auth/login.html', form=form, title='Login')


# @auth.route('/logout')
# @login_required
# def logout():
#     """
#     Handle requests to the /logout route
#     Log an employee out through the logout link
#     """
#     logout_user()
#     flash('You have successfully been logged out.')

#     # redirect to the login page
#     return redirect(url_for('auth.login'))