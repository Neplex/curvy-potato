"""
Main
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_script import Manager
from flask_jwt_extended import JWTManager

from app.config import Config


# Build flask app
APP = Flask(__name__)
# Diable Flask-SQLAlchemy event system
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['JWT_BLACKLIST_ENABLED'] = True
APP.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# Build extensions
CONFIG = Config(APP)
DB = SQLAlchemy(APP)
BCRYPT = Bcrypt(APP)
JWT_MANAGER = JWTManager(APP)
MANAGER = Manager(APP)
