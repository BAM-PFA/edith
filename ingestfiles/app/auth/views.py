import json
import urllib
import uuid

import wtforms
from flask import render_template, url_for, request, redirect, jsonify
from werkzeug import MultiDict

from . import auth
from . import forms
from .. import listObjects


@auth.route('/login',methods=['GET','POST'])
def login():
	# from flask import current_app as app
	print('hooo')
	

	return render_template('index.html',title='Index',objects=objects,form=form)

