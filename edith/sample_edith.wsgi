import sys

# add the directory for EDITH to the system path so mod_wsgi can find it and run the app
sys.path.insert(0,'/path/to/edith/edith')
from edith import app as application
