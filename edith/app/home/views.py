# app/home/views.py
from flask import render_template
from flask_login import login_required, current_user

from .. import utils

from . import home

@home.route('/',methods=['GET','POST'])
def homepage():
	"""
	Render the homepage template on the / route
	"""
	return render_template('home/index.html', title="Welcome", current_user=current_user)

@home.route('/dashboard')
@login_required
def dashboard():
	"""
	Render the dashboard template on the /dashboard route
	"""
	return render_template('home/dashboard.html', title="Dashboard")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/system_menu')
@login_required
def system_menu():
	"""
	Render the system menu
	"""
	return render_template(
		'/home/system_menu.html',
		title = "System Menu"
		)

@home.route('/pymm_log')
@login_required
def pymm_log():
	"""
	Display the pymm log...
	"""
	pymm_log = utils.get_pymm_log()

	return render_template(
		'/home/pymm_log.html',
		pymm_log = pymm_log
		)