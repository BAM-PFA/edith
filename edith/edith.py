#!/usr/bin/env python3
'''
This is the FLASK_APP that runs the show.

First it inits the app based on the __init__.py file,
then runs the thing.
'''

import os

# local stuff
from app import create_app

# run: export FLASK_CONFIG=development/production
config_name = os.getenv('FLASK_CONFIG')
# print(config_name+"HEYYYYYYYYYYYYYY")

app = create_app(config_name)

if __name__ == '__main__':
	app.run()
