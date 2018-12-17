"""
User app object
"""
from datetime import datetime

from app.app import DB, BCRYPT

FAVOURITES = DB.Table('favourites',
                      DB.Column('user_id', DB.Integer, DB.ForeignKey('user.id'), primary_key=True),
                      DB.Column('structure_id', DB.Integer, DB.ForeignKey('structure.id'),
                                primary_key=True))


class User(DB.Model):
    """Describe an application that is registered to use API protected resources."""

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    username = DB.Column(DB.String(250), unique=True, nullable=False)
    password_hash = DB.Column(DB.String(100), nullable=False)
    created_on = DB.Column(DB.DateTime, nullable=False, default=datetime.now)

    structures = DB.relationship('Structure', backref='user')
    favourites = DB.relationship('Structure', secondary=FAVOURITES,
                                 lazy=True, backref=DB.backref('favourites_of', lazy=True))


    @property
    def password(self):
        """The application key can not be read because it is encrypted in the database."""
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, api_key):
        """Store the encrypted version of the application key."""
        self.password_hash = BCRYPT.generate_password_hash(
            api_key).decode('utf-8')

    def check_password(self, password):
        """Check if the given key is the application one."""
        return BCRYPT.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
