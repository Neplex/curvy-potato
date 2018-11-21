"""
User app object
"""

from datetime import datetime

from app import DB, BCRYPT


class UserApp(DB.Model):
    """Describe an application that is registered to use API protected resources."""

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    app_name = DB.Column(DB.String(250), unique=True, nullable=False)
    app_key_hash = DB.Column(DB.String(100), nullable=False)
    created_on = DB.Column(DB.DateTime, nullable=False, default=datetime.now)

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

    def __repr__(self):
        return '<UserApp %r>' % self.app_name
