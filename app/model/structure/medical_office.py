"""
Medical office object
"""

from app.app import DB
from .structure import Structure, StructureType


class MedicalOffice(Structure):
    """Medical office structure"""

    id = DB.Column(DB.Integer, DB.ForeignKey('structure.id'), primary_key=True)
    phone = DB.Column(DB.String)
    specialities = DB.Column(DB.ARRAY(DB.String))

    __mapper_args__ = {'polymorphic_identity': StructureType.MEDICAL_OFFICE}
