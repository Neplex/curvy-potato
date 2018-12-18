"""
Gym object
"""

from app.app import DB
from .structure import Structure, StructureType


class Gym(Structure):
    """Gym structure"""

    id = DB.Column(DB.Integer, DB.ForeignKey('structure.id'), primary_key=True)
    phone = DB.Column(DB.String)
    price = DB.Column(DB.Integer)

    __mapper_args__ = {'polymorphic_identity': StructureType.GYM}
