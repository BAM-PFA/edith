import json
import urllib
import uuid

import wtforms
from flask import render_template, url_for, request, redirect, jsonify
from werkzeug import MultiDict

from . import lto
from . import forms
from .. import listObjects


@lto.route('/lto',methods=['GET','POST'])
def lto():



@lto.route('/lto_id',methods=['GET','POST'])
def lto_id():
	LTOid = forms.LTO_id_form()

	return render_template(
		'lto.html',
		title="LTO id"
		form=LTOid
		)
