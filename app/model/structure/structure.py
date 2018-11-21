"""
Structure object
"""

from sqlalchemy import func
from geoalchemy2 import Geometry

from app import DB


class Structure(DB.Model):
    """Base class for Structures."""

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(50), nullable=False)
    description = DB.Column(DB.String(300))
    geom = DB.Column(Geometry('POINT'), nullable=False)

    @property
    def geometry(self):
        return DB.session.scalar(func.ST_AsGeoJSON(self.geom))

    def __repr__(self):
        return '<Structure %r>' % self.name
