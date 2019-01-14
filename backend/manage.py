import os
from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
import unittest

from main.database import db
from main import create_app 

from main.api.user_api import user_api
from main.api.diet_api import diet_api

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

manager = Manager(app)

# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('main/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()