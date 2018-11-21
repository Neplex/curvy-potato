"""
Hospital object
"""

from app import DB
from . import Structure


class Hospital(Structure):
    """Hospital structure"""

    urgence = DB.Column(DB.Boolean)
    maternite = DB.Column(DB.Boolean)

    def __repr__(self):
        return '<Hospital %r>' % self.name
