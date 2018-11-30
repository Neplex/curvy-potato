"""
Hospital object
"""

from app.app import DB
from .structure import Structure


class Hospital(Structure):
    """Hospital structure"""

    emergency = DB.Column(DB.Boolean)
    maternity = DB.Column(DB.Boolean)

    __mapper_args__ = {'polymorphic_identity': 'hospital'}
