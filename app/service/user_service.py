"""
User service
"""

from sqlalchemy.orm import with_polymorphic

from app.app import DB
from app.model.structure import Structure
from app.model.user import User
from app.service.struct_service import get_structure


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


def get_all_structure_by_user(user_id):
    """Get all structures from user"""
    return DB.session.query(with_polymorphic(Structure, '*')).filter(Structure.user_id == user_id)


def get_favorites_by_user(user_id):
    """Get all favorites of an user"""
    return DB.session.query(with_polymorphic(Structure, '*')).filter(
        Structure.favorites_of.any(id=user_id))

def add_favorite_to_user(user_id, structure_id):
    """Add a favorite to a defined user"""
    user = get_user(user_id)
    struct = get_structure(structure_id)
    user.favorites.append(struct)
    #DB.session.merge(user)
    DB.session.commit()