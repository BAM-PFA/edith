import os

# local stuff
from app import create_app

# export FLASK_CONFIG=development/production
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()