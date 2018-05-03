import json
import urllib
import uuid

import wtforms
from flask import render_template, url_for, request, redirect, jsonify
from werkzeug import MultiDict

from . import lto
from . import forms
from .. import listObjects


@lto.route('/lto_menu',methods=['GET','POST'])
def lto_menu():
	return render_template(
		'lto_menu.html',
		title='LTO MENU'
		)


@lto.route('/lto_id',methods=['GET','POST'])
def lto_id():
	LTOid = forms.LTO_id_form()

	return render_template(
		'lto.html',
		title="LTO id",
		form=LTOid
		)
