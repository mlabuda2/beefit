import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main.database import db
from main import create_app 

from main.api.user_api import user_api
from main.api.diet_api import diet_api

app = create_app()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run(debug=True)