#!/usr/bin/env python3

'''
Taken from https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-two
'''


from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, AddUserForm, EditUserForm, DataSourceForm
from .. import db
from ..models import Department, User, Data_Source


def check_admin():
	"""
	Prevent non-admins from accessing the page
	"""
	if not current_user.is_admin:
		abort(403)

####################
# Department Views
@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
	"""
	List all departments
	"""
	check_admin()

	departments = Department.query.all()

	return render_template(
		'admin/departments/departments.html',
		departments=departments,
		title="Departments"
		)

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
	"""
	Add a department to the database
	"""
	check_admin()

	add_department = True

	form = DepartmentForm()
	if form.validate_on_submit():
		department = Department(
			deptname=form.deptname.data,
			description=form.description.data
			)
		try:
			# add department to the database
			db.session.add(department)
			db.session.commit()
			flash('You have successfully added a new department.')
		except:
			# in case department name already exists
			flash('Error: department name already exists.')

		# redirect to departments page
		return redirect(url_for('admin.list_departments'))

	# load department template
	return render_template(
		'admin/departments/department.html', 
		action="Add",
		add_department=add_department,
		form=form,
		title="Add Department"
		)

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
	"""
	Edit a department
	"""
	check_admin()

	add_department = False

	department = Department.query.get_or_404(id)
	form = DepartmentForm(obj=department)
	if form.validate_on_submit():
		department.deptname = form.deptname.data
		department.description = form.description.data
		db.session.commit()
		flash('You have successfully edited the department.')

		# redirect to the departments page
		return redirect(url_for('admin.list_departments'))

	form.description.data = department.description
	form.deptname.data = department.deptname
	return render_template(
		'admin/departments/department.html', 
		action="Edit",
		add_department=add_department, 
		form=form,
		department=department,
		title="Edit Department"
		)


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
	"""
	Delete a department from the database
	"""
	check_admin()

	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	flash('You have successfully deleted the department.')

	# redirect to the departments page
	return redirect(url_for('admin.list_departments'))

	return render_template(title="Delete Department")

####################
# User Views
@admin.route('/users')
@login_required
def list_users():
	"""
	List all users
	"""
	check_admin()

	users = User.query.all()
	return render_template(
		'admin/users/users.html',
		users=users, 
		title='Users'
		)

@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
	"""
	Add a user to the database
	"""
	check_admin()

	add_user = True

	form = AddUserForm()
	# print(form.data)
	# print("HIIHII")
	if form.validate_on_submit():
		# print(form.department_id.data.id)
		# print(type(form.department_id.data))

		user = User(
			department_id=form.department_id.data.id,
			email=form.email.data,
			username=form.username.data,
			first_name=form.first_name.data,
			last_name=form.last_name.data,
			RSusername=form.RSusername.data,
			RSkey=form.RSkey.data,
			is_admin=form.is_admin.data,
			password=form.password.data
			)
		try:
			# add department to the database
			db.session.add(user)
			# print(user)
			db.session.commit()
			flash('You have successfully added a new user.')
		except Exception as e:
			# in case department name already exists
			# print(str(e))
			flash('Error: user already exists.')

		# redirect to departments page
		return redirect(url_for('admin.list_users'))

	# load department template
	return render_template(
		'admin/users/user.html',
		action="Add",
		add_user=add_user,
		form=form,
		title="Add User"
		)

@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
	"""
	Edit a user
	""" 
	check_admin()

	add_user = False

	user = User.query.get_or_404(id)
	form = EditUserForm(obj=user)
	if form.validate_on_submit():
		# print(form.data)
		if not form.department_id.data == None:
			user.department_id=form.department_id.data.id
		user.email = form.email.data
		user.username = form.username.data
		user.first_name = form.first_name.data
		user.last_name = form.last_name.data
		user.RSusername = form.RSusername.data
		user.RSkey = form.RSkey.data
		user.is_admin = form.is_admin.data
		if form.password.data:
			user.password = form.password.data
		try:
			db.session.commit()
			# print(form.data)
			flash('You have successfully edited the user.')

			# redirect to the users page
			return redirect(url_for('admin.list_users'))
		except Exception as e:
			print(e)
			flash('Error editing the user.')
			return redirect(url_for('admin.list_users'))

	# this pre-populates the form with existing data from the db
	deptID = Department.query.get(user.department_id).id
	print(deptID)
	if not deptID in ('',None,"Null"):
		form.department_id=deptID
	form.email.data = user.email
	form.username.data = user.username
	form.first_name.data = user.first_name
	form.last_name.data = user.last_name 
	form.RSusername.data = user.RSusername
	form.RSkey.data = user.RSkey
	form.is_admin.data = user.is_admin
	return render_template(
		'admin/users/user.html', 
		action="Edit",
		add_user=add_user, 
		form=form,
		user=user,
		title="Edit User"
		)

@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
	"""
	Delete a user from the database
	"""
	check_admin()

	user = User.query.get_or_404(id)
	db.session.delete(user)
	db.session.commit()
	flash('You have successfully deleted the user.')

	# redirect to the users page
	return redirect(url_for('admin.list_users'))

	return render_template(title="Delete User")

####################
# Data Sources Views
@admin.route('/data_sources')
@login_required
def list_data_sources():
	"""
	List all data_sources
	"""
	check_admin()

	data_sources = Data_Source.query.all()
	return render_template('admin/data_sources/data_sources.html',
						   data_sources=data_sources, title='Data_Sources')

@admin.route('/data_sources/add', methods=['GET', 'POST'])
@login_required
def add_data_source():
	"""
	Add a data_source to the database
	"""
	check_admin()

	add_data_source = True

	form = DataSourceForm()
	if form.validate_on_submit():
		data_source = Data_Source(
			dbName = form.dbName.data,
			fmpLayout = form.fmpLayout.data,
			IPaddress = form.IPaddress.data,
			username = form.username.data,
			credentials = form.credentials.data,
			description = form.description.data
			)
		try:
			# add department to the database
			db.session.add(data_source)
			# print(data_source)
			db.session.commit()
			flash('You have successfully added a new data_source.')
		except Exception as e:
			# in case department name already exists
			# print(str(e))
			flash('Error adding data source. {}'.format(e))

		# redirect to departments page
		return redirect(url_for('admin.list_data_sources'))

	# load department template
	return render_template(
		'admin/data_sources/data_source.html',
		action="Add",
		add_data_source=add_data_source,
		form=form,
		title="Add Data Source"
		)

@admin.route('/data_sources/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_data_source(id):
	"""
	Edit a data_source
	""" 
	check_admin()

	add_data_source = False

	data_source = Data_Source.query.get_or_404(id)
	form = DataSourceForm(obj=data_source)
	if form.validate_on_submit():
		# print(form.data)
		data_source.dbName= form.dbName.data,
		data_source.fmpLayout = form.fmpLayout.data
		data_source.IPaddress = form.IPaddress.data
		data_source.username = form.username.data
		data_source.credentials = form.credentials.data
		data_source.description = form.description.data
		try:
			db.session.commit()
			flash('You have successfully edited the data source.')

			# redirect to the users page
			return redirect(url_for('admin.list_data_sources'))
		except Exception as e:
			print(e)
			flash('Error editing the data_source. {}'.format(e))
			return redirect(url_for('admin.list_data_sources'))

	# this pre-populates the form with existing data from the db
	form.dbName.data = data_source.dbName
	form.fmpLayout.data = data_source.fmpLayout
	form.IPaddress.data = data_source.IPaddress
	form.username.data = data_source.username 
	form.credentials.data = data_source.credentials
	form.description.data = data_source.description
	return render_template(
		'admin/data_sources/data_source.html', 
		action="Edit",
		add_data_source=add_data_source, 
		form=form,
		data_source=data_source,
		title="Edit Data Source"
		)

@admin.route('/data_sources/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_data_source(id):
	"""
	Delete a data_source from the database
	"""
	check_admin()

	data_source = Data_Source.query.get_or_404(id)
	db.session.delete(data_source)
	db.session.commit()
	flash('You have successfully deleted the data source.')

	# redirect to the data_sources page
	return redirect(url_for('admin.list_data_sources'))

	return render_template(title="Delete Data Source")
