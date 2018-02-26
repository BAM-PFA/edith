import os

from app import app

def list_objects():
	source = app.config["SHARED_DIR"]
	objects = {}
	for _object in os.listdir(source):
		if not _object.startswith('.'):
			objects[(os.path.join(source,_object))] = _object

	return objects