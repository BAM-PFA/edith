import os

from ingest import ingest

def list_objects():
	source = ingest.config["SHARED_DIR"]
	objects = {}
	for _object in os.listdir(source):
		if not _object.startswith('.'):
			objects[(os.path.join(source,_object))] = _object

	return objects