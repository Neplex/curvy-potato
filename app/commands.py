"""
CLI custom commands
"""

import click
from flask.cli import AppGroup

from app.app import DB, APP
from app.model.user_app import UserApp
from app.service.auth_service import generate_api_key, save_app, remove_app


@APP.cli.command()
@click.option("--init", "option", flag_value="init", help="Initialization of the database.")
@click.option("--delete", "option", flag_value="delete", help="Deletion of the database.")
@click.option("--force", "force", flag_value="force", help="Don't need to confirm.")
def database(option, force):
    """Data base util."""
    if option == 'init':
        DB.create_all()

    elif option == 'delete' \
            and (force == 'force' or click.confirm('Are you sure you want to delete the database')):
        DB.drop_all()


# Command group for user app
APP_GROUP = AppGroup("app", help="App management.")


@APP_GROUP.command("add")
@click.argument("app_name")
def add_app(app_name):
    """Add a new user app"""
    api_key = generate_api_key()
    user_app = UserApp(app_name=app_name, app_key=api_key)
    save_app(user_app)
    print("""
    New app added:
    name: %s
    key: %s
        (Warning, this key is private and cannot be restored)
    """ % (app_name, api_key))


@APP_GROUP.command("delete")
@click.argument("app_name")
def delete_app(app_name):
    """Delete an user app"""
    remove_app(app_name)


# Add group to cli
APP.cli.add_command(APP_GROUP)
