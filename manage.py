import os
import unittest
from pathlib import Path
from dotenv import load_dotenv

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

ENV = os.getenv('BOILERPLATE_ENV') or 'dev'
env_path = Path('.') / ('.env.' + ENV)
load_dotenv(dotenv_path=env_path)

from app import blueprint
from app.main import create_app, db
from app.main.model import user

app = create_app(ENV)
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

# Max 4 MB
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
