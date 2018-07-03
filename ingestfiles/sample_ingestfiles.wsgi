import sys

# add the directory for ingestfiles to the system path so mod_wsgi can find it and run the app
sys.path.insert(0,'/path/to/ingestfiles/ingestfiles')
from ingestfiles import app as application
