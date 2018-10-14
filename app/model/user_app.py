"""
User app object
"""

import datetime
import jwt

from .. import APP, DB, BCRYPT


class UserApp(DB.Model):
    """Describe an application that is registered to use API protected resources."""

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    app_name = DB.Column(DB.String(250), unique=True, nullable=False)
    app_key_hash = DB.Column(DB.String(100), nullable=False)
    created_on = DB.Column(DB.DateTime, nullable=False)

    def __init__(self, name, key):
        self.app_name = name
        self.app_key = key

    @property
    def app_key(self):
        """The application key can not be read because it is encrypted in the database."""
        raise AttributeError('app_key: write-only field')

    @app_key.setter
    def app_key(self, api_key):
        """Store the encrypted version of the application key."""
        self.app_key_hash = BCRYPT.generate_password_hash(
            api_key).decode('utf-8')

    def check_app_key(self, app_key):
        """Check if the given key is the application one."""
        return BCRYPT.check_password_hash(self.app_key_hash, app_key)

    def encode_auth_token(self):
        """Get a JWT token for the application."""
        return jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
        }, APP.secret_key, algorithm='HS256')

    @staticmethod
    def decode_auth_token(auth_token):
        """Revoke a JWT token."""
        try:
             # TODO: return an user application instead of id
            return jwt.decode(auth_token, APP.secret_key)['sub']

        # TODO: Get rid of string return, generate an error instead.
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'

        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<UserApp %r>' % self.app_name
