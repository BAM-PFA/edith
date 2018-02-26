from app import app, listObjects, forms
from flask import render_template, url_for, request, redirect

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
	DIR = app.config["SHARED_DIR"] 
	objects = listObjects.list_objects()
	form = forms.IngestForm()

	if form.is_submitted():
		print("HEY")
		result = form.data
		print(result)
		# for item in form.data.items():
		# 	print(item)
		# print(extra)
		# return render_template('status.html',title='Ingest',data=data,extra=extra)

		return redirect(url_for('status'))
	return render_template('index.html',title='Index',objects=objects,form=form)

@app.route('/status',methods=['GET','POST'])
def status():
	status = 'OK'
	print(status)
	try:
		items = 'stuff'
		data = request.form.to_dict(flat=False)
		# extra = form.targetObject.data
		extra = 'LKWELKLN'
		# print(data)
	except:
		data = "no data"
		extra = ":("
		items = "POPOP"
		# print(data)
	return render_template('status.html',title='Ingest',data=data,extra=extra)

	