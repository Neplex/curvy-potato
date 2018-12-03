"""
Main
"""

import os

from flask import Flask, redirect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Build flask app
APP = Flask(__name__)
# Diable Flask-SQLAlchemy event system
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['JWT_BLACKLIST_ENABLED'] = True
APP.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
APP.config['DEBUG'] = os.getenv('DEBUG', 'False')
APP.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))

# Build extensions
DB = SQLAlchemy(APP)
BCRYPT = Bcrypt(APP)
JWT_MANAGER = JWTManager(APP)


@APP.route('/')
def home():
    """Home page to avoid 404"""
    return redirect('/v1')
