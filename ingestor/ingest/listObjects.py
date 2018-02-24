import os

from ingest import ingest

def list_objects():
	objects = []
	for _object in os.listdir(ingest.config["SHARED_DIR"]):
		objects.append(_object)

	return objects