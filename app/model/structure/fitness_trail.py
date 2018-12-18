"""
Fitness trail object
"""

from sqlalchemy import func

from app.app import DB
from .structure import Structure, StructureType


class FitnessTrail(Structure):
    """Fitness trail structures."""

    id = DB.Column(DB.Integer, DB.ForeignKey('structure.id'), primary_key=True)
    difficulty = DB.Column(DB.Integer)

    __mapper_args__ = {'polymorphic_identity': StructureType.FITNESS_TRAIL}

    @property
    def length(self):
        """The length can only be read because it's compute from the trace."""
        return DB.session.scalar(func.ST_Length(self.geom))
