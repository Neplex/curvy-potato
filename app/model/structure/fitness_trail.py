"""
Fitness trail object
"""

from sqlalchemy import func

from app.app import DB
from .structure import Structure


class FitnessTrail(Structure):
    """Fitness trail structures."""

    difficulty = DB.Column(DB.Integer)

    __mapper_args__ = {'polymorphic_identity': 'fitness_trail'}

    @property
    def length(self):
        """The length can only be read because it's compute from the trace."""
        return DB.session.scalar(func.ST_Length(self.geom))
