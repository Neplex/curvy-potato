"""
Manager commands
"""

from flask_script import prompt_bool

from app import MANAGER, DB
from app.model.user_app import UserApp
from app.service.auth_service import generate_api_key, save_app, remove_app


@MANAGER.command
def db(arg):
    """Data base util"""

    if arg == 'init':
        DB.create_all()

    elif arg == 'delete' and prompt_bool('Are you sure you want to delete the database'):
        DB.drop_all()

    else:
        print("""Invalid command, try:
        - init
        - delete""")


@MANAGER.command
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


@MANAGER.command
def delete_app(app_name):
    """Delete an user app"""
    remove_app(app_name)
