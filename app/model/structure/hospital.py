"""
Hospital object
"""

from app.app import DB
from .structure import Structure, StructureType


class Hospital(Structure):
    """Hospital structure"""

    id = DB.Column(DB.Integer, DB.ForeignKey('structure.id'), primary_key=True)
    phone = DB.Column(DB.String)
    emergency = DB.Column(DB.Boolean)
    maternity = DB.Column(DB.Boolean)

    __mapper_args__ = {'polymorphic_identity': StructureType.HOSPITAL}
