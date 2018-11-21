"""
Fitness trail object
"""

from sqlalchemy import func
from geoalchemy2 import Geometry

from app import DB
from . import Structure


class FitnessTrail(Structure):
    """Fitness trail structures."""

    difficulty = DB.Column(DB.Integer)
    trace = DB.Column(Geometry('MULTILINESTRING'))

    @property
    def length(self):
        """The length can only be read because it's compute from the trace."""
        return self.filter(func.ST_Length)

    def __repr__(self):
        return '<FitnessTrail %r>' % self.name
