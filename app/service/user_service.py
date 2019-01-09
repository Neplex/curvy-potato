"""
User service
"""

from sqlalchemy.orm import with_polymorphic
from werkzeug.exceptions import NotFound

from app.app import DB
from app.model.structure import Structure
from app.model.user import User
from app.service.struct_service import get_structure


class UserNotFound(NotFound):
    """Structure not found Exception. Raised when a structure is not in DB"""

    def __init__(self, user_id):
        super().__init__("User {} doesn't exist".format(user_id))


def get_all_user():
    """Get all users."""
    return DB.session.query(User).all()


def add_user(user):
    """Add a new user."""
    DB.session.add(user)
    DB.session.commit()


def get_user(user_id):
    """Get a user from id"""
    user = User.query.get(user_id)
    if user is None:
        raise UserNotFound(user_id)
    return user


def update_user(user):
    """Update a defined user"""
    DB.session.merge(user)
    DB.session.commit()


def delete_user(user_id):
    """Delete a defined user"""
    user = get_user(user_id)
    DB.session.delete(user)
    DB.session.commit()


def get_all_structure_by_user(user_id):
    """Get all structures from user"""
    user = get_user(user_id)
    return DB.session.query(with_polymorphic(Structure, '*')).filter(Structure.user_id == user.id)


def get_favorites_by_user(user_id):
    """Get all favorites of an user"""
    user = get_user(user_id)
    return DB.session.query(with_polymorphic(Structure, '*')).filter(
        Structure.favorites_of.any(id=user.id))


def add_favorite_to_user(user_id, structure_id):
    """Add a favorite to a defined user"""
    user = get_user(user_id)
    structure = get_structure(structure_id)
    user.favorites.append(structure)
    DB.session.commit()


def delete_favorite(user_id, favorite_id):
    """Delete a favorite for an user"""
    user = get_user(user_id)
    structure = get_structure(favorite_id)
    user.favorites.remove(structure)
    DB.session.commit()
