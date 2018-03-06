import os

import app

def list_objects():
	source = app.app_config["SHARED_DIR"]
	objects = {}
	for _object in os.listdir(source):
		if not _object.startswith('.'):
			objects[(os.path.join(source,_object))] = _object

	return objects