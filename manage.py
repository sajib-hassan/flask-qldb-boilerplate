import os
import unittest

import click
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from hash_chain.app import create_app
from hash_chain.app.extensions import db
from hash_chain.app.modules.users.models import User

app = create_app(os.getenv('HASH_CHAIN_ENV', 'development'))

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


def add_user_from_cli(data):
    if User.find_by_email(data["email"]):
        error = f"Error: {data['email']} is already registered"
        click.secho(f"{error}\n", fg="red", bold=True)
        return 1
    new_user = User(data)
    db.session.add(new_user)
    db.session.commit()
    user_type = "admin user" if data["admin"] else "user"
    message = f"Successfully added new {user_type}:\n {new_user}"
    click.secho(message, fg="blue", bold=True)


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('hash_chain/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
@manager.option('-a', '--admin', dest='admin', default=True)
@manager.option('-u', '--username', dest='username', default=None)
def add_admin(email, password, admin, username):
    add_user_from_cli(email=email, password=password, admin=admin, username=username)


@manager.command
def seed_users():
    """Runs the seed users."""
    _data = dict(
        email='joe_admin@gmail.com',
        username='joe_admin',
        password='admin',
        admin=True
    )
    add_user_from_cli(data=_data)
    _data = dict(
        email='joe@gmail.com',
        username='jeo',
        password='user',
        admin=False
    )
    add_user_from_cli(data=_data)


if __name__ == '__main__':
    manager.run()
