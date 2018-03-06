import os

# from app import config
import app

print(dir(app))
# from flask import current_app as app
def list_objects():
	# from flask import current_app as app
	source = app.app_config["SHARED_DIR"]
	objects = {}
	for _object in os.listdir(source):
		if not _object.startswith('.'):
			objects[(os.path.join(source,_object))] = _object

	return objects