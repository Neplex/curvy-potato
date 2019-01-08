"""
CLI custom commands
"""

import click
from flask.cli import AppGroup

from app.app import DB, APP
from app.model.user import User
from app.model.structure import FitnessTrail, Hospital
from app.service.auth_service import save_user, remove_user
from app.service.struct_service import add_structure


@APP.cli.command()
@click.option("--init", "option", flag_value="init", help="Initialization of the database.")
@click.option("--delete", "option", flag_value="delete", help="Deletion of the database.")
@click.option("--populate", "option", flag_value="populate", help="Populate the database.")
@click.option("--force", "force", flag_value="force", help="Don't need to confirm.")
def database(option, force):
    """Data base util."""
    if option == 'init':
        DB.create_all()

    elif option == 'delete' \
            and (force == 'force' or click.confirm('Are you sure you want to delete the database')):
        DB.drop_all()

    elif option == 'populate':
        user = User(username="string", password="string")
        struct = FitnessTrail(name="fitness trail", description="trail",
                              difficulty=10, geom="LINESTRING(30 10, 20 20)",
                              user_id=1)
        user.favorites.append(struct)
        save_user(user)
        add_structure(struct)
        struct = Hospital(name="hospital", description="some hospital",
                          emergency=True, maternity=False, geom="POINT(10 10)",
                          user_id=1)
        add_structure(struct)


# Command group for user app
USER_GROUP = AppGroup("user", help="User management.")


@USER_GROUP.command("add")
@click.argument("username")
@click.argument("password")
def add_user(username, password):
    """Add a new user"""
    user = User(username=username, password=password)
    save_user(user)
    print("""New user added:
    username: %s
    password: %s""" % (username, password))


@USER_GROUP.command("delete")
@click.argument("username")
def delete_user(username):
    """Delete an user"""
    remove_user(username)


# Add group to cli
APP.cli.add_command(USER_GROUP)
