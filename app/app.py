"""
Main
"""

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restplus import Api
from flask_script import Manager

from .config import Config
from .controller.auth_controller import API as auth_ns


# Build flask app
APP = Flask(__name__)
# Diable Flask-SQLAlchemy event system
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Build extensions
CONFIG = Config(APP)
DB = SQLAlchemy(APP)
BCRYPT = Bcrypt(APP)
MANAGER = Manager(APP)

# API v1
API_BLUEPRINT = Blueprint('api', __name__, url_prefix='/v1')
API = Api(API_BLUEPRINT, title='', version='1.0', description='')

API.add_namespace(auth_ns)

# Register blueprints
APP.register_blueprint(API_BLUEPRINT)
APP.app_context().push()
