"""
User service
"""


from app.app import DB
from app.model.user import User

def get_all_user():
    """Get all users."""
    return DB.session.query(User).all()


def add_user(user):
    """Add a new user."""
    DB.session.add(user)
    DB.session.commit()


def get_user(user_id):
    """Get a user from id"""
    return User.query.get(user_id)


def update_user(user):
    """Update a defined user"""
    DB.session.merge(user)
    DB.session.commit()


def delete_user(user_id):
    """Delete a defined user"""
    user = get_user(user_id)
    if user is not None:
        DB.session.delete(user)
        DB.session.commit()
