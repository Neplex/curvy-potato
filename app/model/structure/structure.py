"""
Structure object
"""

import geojson
from geoalchemy2 import Geometry
from sqlalchemy import func

from app.app import DB


class Structure(DB.Model):
    """Base class for Structures."""

    # __abstract__ = True

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(50), nullable=False)
    description = DB.Column(DB.String(300))
    structure_type = DB.Column(DB.String)
    geom = DB.Column(Geometry, nullable=False)

    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"))


    __mapper_args__ = {'polymorphic_on': structure_type}

    @property
    def geometry(self):
        """Get geometry as geojson object"""
        return geojson.loads(DB.session.scalar(func.ST_AsGeoJSON(self.geom)))

    @geometry.setter
    def geometry(self, geometry):
        self.geom = func.ST_GeomFromGeoJSON(geometry)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)
