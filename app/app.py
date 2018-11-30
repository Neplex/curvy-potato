"""
Main
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os


# Build flask app
APP = Flask(__name__)
# Diable Flask-SQLAlchemy event system
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['JWT_BLACKLIST_ENABLED'] = True
APP.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
APP.config['DEBUG'] = os.getenv('DEBUG')
APP.config['SECRET_KEY'] = os.getenv('SECRET_KEY',os.urandom(24))

# Build extensions
DB = SQLAlchemy(APP)
BCRYPT = Bcrypt(APP)
JWT_MANAGER = JWTManager(APP)
