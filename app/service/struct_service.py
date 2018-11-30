"""
Structure service
"""

from sqlalchemy.orm import with_polymorphic

from app.app import DB
from app.model.structure import Structure


def get_all_structure():
    """Get all structures."""
    return DB.session.query(with_polymorphic(Structure, '*'))


def add_structure(struct):
    """Add a structure in the database."""
    DB.session.add(struct)
    DB.session.commit()


def get_structure(structure_id):
    """Get a structure from the DB given its identifier"""
    return Structure.query.get(structure_id)


def delete_structure(structure_id):
    """Delete a structure from the DB given its identifier"""
    struct = get_structure(structure_id)

    if struct is not None:
        DB.session.delete(struct)
        DB.session.commit()
